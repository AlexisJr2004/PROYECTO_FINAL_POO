import json
from datetime import date, timedelta
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from app.core.models import Product, Notification
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.mixins.mixins import PermissionMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, ListViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from decimal import Decimal
from proy_sales.utils import custom_serializer, save_audit

class SaleListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')  # Ver búsqueda
        if q1 is not None:
            self.query.add(Q(id=q1), Q.OR) 
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR) 
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sales:sales_create')
        return context

class SaleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'add_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        context['detail_sales'] = []
        context['save_url'] = reverse_lazy('sales:sales_create') 
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            error_message = f"Error al grabar la venta!!!: {form.errors}."
            messages.error(self.request, error_message)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": form.errors}, status=400)
        
        data = request.POST
        try:
            with transaction.atomic():
                sale = Invoice.objects.create(
                    customer_id=int(data['customer']),
                    payment_method_id=int(data['payment_method']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    discount=Decimal(data['discount']),
                    iva=Decimal(data['iva']),
                    total=Decimal(data['total']),
                    payment=Decimal(data['payment']),
                    change=Decimal(data['change']),
                    state='F'
                )
                details = json.loads(request.POST['detail'])
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "A")
                success_message = f"Éxito al registrar la venta F#{sale.id}"
                messages.success(self.request, success_message)
                Notification.objects.create(message=success_message)
                return JsonResponse({"msg": "Éxito al registrar la venta Factura"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": error_message}, status=400)

class SaleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'change_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        detail_sale = list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
            "product", "product__description", "quantity", "price", "subtotal", "iva"))
        detail_sale = json.dumps(detail_sale, default=custom_serializer)
        context['detail_sales'] = detail_sale
        context['save_url'] = reverse_lazy('sales:sales_update', kwargs={"pk": self.object.id})
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            error_message = f"Error al actualizar la venta!!!: {form.errors}."
            messages.error(self.request, error_message)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": form.errors}, status=400)
        
        data = request.POST
        try:
            sale = Invoice.objects.get(id=self.kwargs.get('pk'))
            today = date.today()

            # Verifica si la fecha de la factura es el mismo día
            if sale.issue_date.date() != today:
                error_message = 'Solo puedes modificar ventas del mismo día.'
                messages.error(self.request, error_message)
                Notification.objects.create(message=error_message)
                return JsonResponse({"msg": error_message}, status=400)

            with transaction.atomic():
                sale.customer_id = int(data['customer'])
                sale.payment_method_id = int(data['payment_method'])
                sale.issue_date = data['issue_date']
                sale.subtotal = Decimal(data['subtotal'])
                sale.discount = Decimal(data['discount'])
                sale.iva = Decimal(data['iva'])
                sale.total = Decimal(data['total'])
                sale.payment = Decimal(data['payment'])
                sale.change = Decimal(data['change'])
                sale.state = 'M'
                sale.save()
                
                # Eliminar detalles existentes y restaurar stock
                detdelete = InvoiceDetail.objects.filter(invoice_id=sale.id)
                for det in detdelete:
                    det.product.stock += Decimal(det.quantity)
                    det.product.save()
                detdelete.delete()
                
                # Agregar nuevos detalles
                details = json.loads(request.POST['detail'])
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "M")
                success_message = f"Éxito al modificar la venta F#{sale.id}"
                messages.success(self.request, success_message)
                Notification.objects.create(message=success_message)
                return JsonResponse({"msg": "Éxito al modificar la venta Factura"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": error_message}, status=400)

class SaleAnnulView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'core/delete.html'
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'change_invoice'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annul_url'] = reverse_lazy('sales:sales_annul', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        invoice = self.get_object()
        today = date.today()
        max_annul_date = today - timedelta(days=3)

        if invoice.issue_date.date() < max_annul_date:
            error_message = 'Solo puedes anular ventas realizadas hasta 3 días antes.'
            messages.error(self.request, error_message)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": error_message}, status=400)

        try:
            with transaction.atomic():
                invoice.active = False
                invoice.state = 'A'
                invoice.save()
                
                details = InvoiceDetail.objects.filter(invoice=invoice)
                for detail in details:
                    product = detail.product
                    product.stock += detail.quantity
                    product.save()
                
                save_audit(request, invoice, "A")
                success_message = f"Éxito al anular la venta F#{invoice.id}"
                messages.success(self.request, success_message)
                Notification.objects.create(message=success_message)
                return JsonResponse({"msg": "Éxito al anular la venta Factura"}, status=200)
        except Exception as ex:
            error_message = str(ex)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": error_message}, status=400)


class SaleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Invoice
    template_name = 'core/delete.html'
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'delete_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Venta'
        context['description'] = f"¿Desea eliminar la venta: {self.object.id}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        today = date.today()

        if self.object.issue_date.date() != today:
            error_message = 'Solo puedes eliminar ventas del mismo día.'
            messages.error(self.request, error_message)
            Notification.objects.create(message=error_message)
            return JsonResponse({"msg": error_message}, status=400)

        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente la venta {self.object.id}."
        messages.success(self.request, success_message)
        Notification.objects.create(message=success_message)
        self.object.delete()
        return super().delete(request, *args, **kwargs)
