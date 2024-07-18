import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
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

from proy_sales.utils import custom_serializer, save_audit

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
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'change_purchase'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issue_date.date() != timezone.now().date():
            messages.error(self.request, "No se puede modificar una compra que no sea del día actual.")
            return JsonResponse({"msg": "No se puede modificar una compra que no sea del día actual."}, status=403)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'cost' ,'price', 'stock', 'iva__value')
        detail_purchase = list(PurchaseDetail.objects.filter(purchase_id=self.object.id).values(
            "product", "product__description", "quantify", "cost", "subtotal", "iva"))
        context['detail_purchases'] = json.dumps(detail_purchase, default=custom_serializer)
        context['save_url'] = reverse_lazy('purchases:purchases_update', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issue_date.date() != timezone.now().date():
            messages.error(self.request, "No se puede modificar una compra que no sea del día actual.")
            return JsonResponse({"msg": "No se puede modificar una compra que no sea del día actual."}, status=403)

        form = self.get_form()
        if not form.is_valid():
            messages.error(self.request, f"Error al actualizar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        
        data = request.POST
        try:
            with transaction.atomic():
                # Revertir las cantidades de los productos comprados anteriormente
                old_details = PurchaseDetail.objects.filter(purchase_id=self.object.id)
                for old_detail in old_details:
                    product = old_detail.product
                    product.stock -= old_detail.quantify
                    product.save()

                self.object.num_document = data['num_document']
                self.object.supplier_id = int(data['supplier'])
                self.object.issue_date = data['issue_date']
                self.object.subtotal = Decimal(data['subtotal'])
                self.object.iva = Decimal(data['iva'])
                self.object.total = Decimal(data['total'])
                self.object.active = True
                self.object.save()
                
                # Eliminar los detalles antiguos
                old_details.delete()

                # Crear nuevos detalles y actualizar el stock de los productos
                details = json.loads(request.POST['detail'])
                for detail in details:
                    product = Product.objects.get(id=int(detail['id']))
                    quantity = Decimal(detail['stock'])
                    
                    PurchaseDetail.objects.create(
                        purchase=self.object,
                        product=product,
                        quantify=quantity,
                        cost=Decimal(detail['cost']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['subtotal']),
                    )
                    
                    # Actualizar el stock del producto
                    product.stock += quantity
                    product.save()

                save_audit(request, self.object, "M")
                messages.success(self.request, f"Éxito al modificar la compra {self.object.num_document}")
                return JsonResponse({"msg": "Éxito al modificar la compra"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            error_traceback = traceback.format_exc()
            print(f"Error: {error_message}")
            print(f"Traceback: {error_traceback}")
            return JsonResponse({"msg": error_message}, status=400)

class PurchaseAnnulView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Purchase
    template_name = 'core/delete.html'
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'delete_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Anular Compra'
        context['description'] = f"¿Desea anular la compra {self.object.num_document}?"
        context['back_url'] = self.success_url
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_date = timezone.now()

        if (current_date - self.object.issue_date).days > 3:
            messages.error(self.request, "No se puede anular la compra ya que han pasado más de 3 días desde su registro.")
            return HttpResponseRedirect(self.get_success_url())
            # return HttpResponseForbidden("No se puede anular la compra ya que han pasado más de 3 días desde su registro.")
        
        # Anular la compra
        self.object.annul()
        
        # Revertir los cambios en el inventario
        purchase_details = self.object.purchase_detail.all()
        for detail in purchase_details:
            product = detail.product
            product.stock -= detail.quantify
            product.save()

        success_message = f"Éxito al anular la compra {self.object.num_document}."
        messages.success(self.request, success_message)
        return HttpResponseRedirect(self.get_success_url())
    
class PurchaseDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Purchase
    template_name = 'core/delete.html'
    success_url = reverse_lazy('purchases:purchases_list')
    permission_required = 'delete_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Compra'
        context['description'] = f"¿Desea eliminar la compra {self.object.num_document}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        current_date = timezone.now()

        # Verificar si la compra fue realizada el mismo día
        if self.object.issue_date.date() != current_date.date():
            messages.error(self.request, "Solo se puede eliminar la compra el mismo día en que fue realizada.")
            return HttpResponseRedirect(self.success_url)
        
        # Anular cambios en el inventario
        purchase_details = self.object.purchase_detail.all()
        for detail in purchase_details:
            product = detail.product
            product.stock -= detail.quantify
            product.save()

        success_message = f"Éxito al eliminar la compra {self.object.num_document}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    