import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy, reverse
from app.core.models import Product
from app.purchases.models import Purchase, PurchaseDetail
from app.purchases.forms.purchase import PurchaseForm
from app.core.models import Product
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, F
from decimal import Decimal
import traceback
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db import transaction
from django.shortcuts import get_object_or_404
import pytz
from proy_sales.utils import custom_serializer, save_audit
from django.conf import settings

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchases/list.html'
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(id=q1), Q.OR)
            self.query.add(Q(supplier__name__icontains=q1), Q.OR)
        queryset = self.model.objects.filter(self.query).order_by('id')
        
        # Añadir un campo para indicar si han pasado más de 3 días
        current_date = timezone.localtime()
        for purchase in queryset:
            purchase.can_modify = purchase.issue_date.date() == current_date.date()
            purchase.can_annul = (current_date - purchase.issue_date) <= timedelta(days=3)
            purchase.can_delete = purchase.issue_date.date() == current_date.date()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchases:purchase_create')
        return context

class PurchaseCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Purchase
    template_name = 'purchases/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'add_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'cost' ,'price', 'stock', 'iva__value')
        context['detail_purchases'] = []
        context['save_url'] = reverse_lazy('purchases:purchases_create')
        last_purchase = Purchase.objects.order_by('-id').first()
        next_id = last_purchase.id + 1 if last_purchase else 1
        context['next_purchase_id'] = next_id
        context['success_url'] = reverse('purchases:purchases_list')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.success(self.request, f"Error al grabar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        data = request.POST
        try:
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    num_document=data['num_document'],
                    supplier_id=int(data['supplier']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    iva=Decimal(data['iva']),
                    total=Decimal(data['total']),
                    active=True
                )
                details = json.loads(request.POST['detail'])
                for detail in details:
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product_id=int(detail['id']),
                        quantify=Decimal(detail['stock']),
                        cost=Decimal(detail['cost']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['subtotal']),
                    )
                    product = Product.objects.get(id=int(detail['id']))
                    product.increase_stock(Decimal(detail['stock']))
                save_audit(request, purchase, "A")
                messages.success(self.request, f"Éxito al registrar la compra {purchase.num_document}")
                return JsonResponse({"msg": "Éxito al registrar la compra"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            error_traceback = traceback.format_exc()
            print(f"Error: {error_message}")
            print(f"Traceback: {error_traceback}")
            return JsonResponse({"msg": error_message}, status=400)

class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'purchases/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchases:purchases/list')
    permission_required = 'change_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'cost', 'price', 'stock', 'iva__value')
        detail_purchase = list(PurchaseDetail.objects.filter(purchase_id=self.object.id).values(
            "product", "product__description", "quantify", "cost", "subtotal", "iva"))
        context['detail_purchases'] = json.dumps(detail_purchase, default=custom_serializer)
        context['save_url'] = reverse_lazy('purchases:purchases_update', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            print("Form errors:", form.errors)
            return JsonResponse({"msg": form.errors.as_json()}, status=400)

        data = request.POST
        try:
            purchase = self.get_object()
            tz = pytz.timezone(settings.TIME_ZONE)
            today = timezone.now().astimezone(tz).date()
            purchase_date = purchase.issue_date.astimezone(tz).date()
            print(f"Today's date: {today}")
            print(f"Purchase date: {purchase_date}")
            if purchase_date != today:
                error_message = f'Solo puedes modificar compras del mismo día. Fecha de compra: {purchase_date}, Fecha actual: {today}'
                return JsonResponse({"msg": error_message}, status=400)

            with transaction.atomic():
                # Guarda los detalles originales
                original_details = {detail.product_id: detail.quantify for detail in purchase.purchase_detail.all()}

                # Actualiza los campos de la compra
                purchase.num_document = data['num_document']
                purchase.supplier_id = int(data['supplier'])
                purchase.issue_date = data['issue_date']
                purchase.subtotal = Decimal(data['subtotal'].replace(',', '.'))
                purchase.iva = Decimal(data['iva'].replace(',', '.'))
                purchase.total = Decimal(data['total'].replace(',', '.'))
                purchase.save()

                # Procesa los detalles
                new_details = json.loads(data['detail'])
                
                # Elimina los detalles existentes
                purchase.purchase_detail.all().delete()

                # Crea los nuevos detalles y actualiza el stock
                for detail in new_details:
                    product_id = int(detail['id'])
                    new_quantity = Decimal(str(detail['stock']))
                    
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product_id=product_id,
                        quantify=new_quantity,
                        cost=Decimal(str(detail['cost'])),
                        subtotal=Decimal(str(detail['subtotal'])),
                        iva=Decimal(str(detail['iva']))
                    )
                    
                    product = Product.objects.get(id=product_id)
                    old_quantity = original_details.get(product_id, 0)
                    quantity_difference = new_quantity - old_quantity
                    product.increase_stock(quantity_difference)

                save_audit(request, purchase, "A")
                messages.success(request, f"Éxito al modificar la compra {purchase.num_document}")
                return JsonResponse({"msg": "Éxito al modificar la compra"}, status=200)

        except Exception as ex:
            print("Exception:", str(ex))
            print("Traceback:", traceback.format_exc())
            return JsonResponse({"msg": str(ex)}, status=400)
        
class PurchaseAnnulView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'core/delete.html'
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'change_purchase'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annul_url'] = reverse_lazy('purchases:purchases_annul', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        purchase = self.get_object()
        today = timezone.now().date()
        max_annul_date = today - timedelta(days=3)

        if purchase.issue_date.date() < max_annul_date:
            error_message = 'Solo puedes anular compras realizadas hasta 3 días antes.'
            messages.error(self.request, error_message)
            return JsonResponse({"msg": error_message}, status=400)

        try:
            with transaction.atomic():
                purchase.active = False
                purchase.state = 'A'
                purchase.save()
                
                # Revertir los cambios en el inventario
                purchase_details = PurchaseDetail.objects.filter(purchase=purchase)
                for detail in purchase_details:
                    product = detail.product
                    product.stock += detail.quantify
                    product.save()
                
                messages.success(self.request, f"Éxito al anular la compra {purchase.num_document}.")
                return JsonResponse({"msg": "Éxito al anular la compra"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            return JsonResponse({"msg": error_message}, status=400)
    
    
class PurchaseDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Purchase
    template_name = 'core/delete.html'
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'delete_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Compra'
        context['description'] = f"¿Desea eliminar la compra: {self.object.num_document}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        purchase = self.get_object()
        today = timezone.now().date()

        if purchase.issue_date.date() != today:
            error_message = 'Solo puedes eliminar compras del mismo día.'
            messages.error(self.request, error_message)
            return JsonResponse({"msg": error_message}, status=400)

        try:
            purchase.delete()
            messages.success(self.request, f"Éxito al eliminar lógicamente la compra {purchase.num_document}.")
            return JsonResponse({"msg": "Éxito al eliminar la compra"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            return JsonResponse({"msg": error_message}, status=400)
