from django.urls import reverse_lazy
from app.core.forms.product_price import ProductPriceForm
from app.core.models import ProductPrice, Product
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import (
    CreateViewMixin,
    DeleteViewMixin,
    ListViewMixin,
    PermissionMixin,
    UpdateViewMixin,
)
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from app.core.models import Notification
from decimal import Decimal 
from django.http import JsonResponse
import json

class ProductPriceListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/product_prices/list.html"
    model = ProductPrice
    context_object_name = "product_prices"
    permission_required = "view_product_price"

    def get_queryset(self):
        q1 = self.request.GET.get("q")
        queryset = self.model.objects.all()
        if q1:
            queryset = queryset.filter(
                Q(product__description__icontains=q1) |
                Q(line__description__icontains=q1) |
                Q(value__icontains=q1)
            )
        return queryset.order_by("-issue_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("core:product_price_create")
        return context

class ProductPriceCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ProductPrice
    template_name = "core/product_prices/form.html"
    form_class = ProductPriceForm
    success_url = reverse_lazy("core:product_price_list")
    permission_required = "add_product_price"

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product_prices = json.loads(request.POST.get('product_prices'))
                for price_data in product_prices:
                    product = Product.objects.get(id=price_data['product_id'])
                    current_price = product.price
                    
                    # Calcula el nuevo precio
                    if price_data['type_increment'] == 'P':
                        new_price = current_price * (1 + Decimal(price_data['value']) / 100)
                    else:
                        new_price = current_price + Decimal(price_data['value'])
                    
                    # Crea el nuevo ProductPrice
                    ProductPrice.objects.create(
                        product=product,
                        line=product.line,
                        type_increment=price_data['type_increment'],
                        value=Decimal(price_data['value']),
                        issue_date=price_data['issue_date'],
                        observation=price_data['observation'],
                        state='A'
                    )
                    
                    # Actualiza el precio del producto
                    product.price = new_price
                    product.save()

                messages.success(request, "Precios de productos actualizados correctamente.")
                return JsonResponse({'success': True, 'redirect_url': self.success_url})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Precio de producto creado correctamente.")
        return response

class ProductPriceCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ProductPrice
    template_name = "core/product_prices/form.html"
    form_class = ProductPriceForm
    success_url = reverse_lazy("core:product_price_list")
    permission_required = "add_product_price"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grabar"] = "Grabar Precio de Producto"
        context["back_url"] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product_prices = request.POST.get('product_prices')
                if product_prices:
                    product_prices = json.loads(product_prices)

                    for price_data in product_prices:
                        product_id = price_data.get('product_id')
                        type_increment = price_data.get('type_increment')
                        value = Decimal(price_data.get('value'))
                        issue_date = price_data.get('issue_date')
                        observation = price_data.get('observation')

                        product = Product.objects.get(id=product_id)
                        old_price = product.price

                        if type_increment == 'P':
                            new_price = old_price * (1 + value / 100)
                        else:
                            new_price = old_price + value

                        ProductPrice.objects.create(
                            product=product,
                            line=product.line,
                            type_increment=type_increment,
                            value=value,
                            issue_date=issue_date,
                            observation=observation,
                            state='A'
                        )

                        # Update product price
                        product.price = new_price
                        product.save()

                    messages.success(request, "Precios de productos actualizados correctamente.")
                    return JsonResponse({'success': True, 'redirect_url': self.success_url})

            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Precio de producto creado correctamente.")
        return response

class ProductPriceUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ProductPrice
    template_name = "core/product_prices/form.html"
    form_class = ProductPriceForm
    success_url = reverse_lazy("core:product_price_list")
    permission_required = "change_product_price"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Actualizar Precio de Producto"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        product_price = self.object
        success_message = f"Éxito al actualizar el precio de producto {product_price.product}."
        messages.success(self.request, success_message)
        Notification.objects.create(message=success_message)
        return response


class ProductPriceDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ProductPrice
    template_name = "core/delete.html"
    success_url = reverse_lazy("core:product_price_list")
    permission_required = "delete_product_price"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Precio de Producto"
        context["description"] = f"¿Desea Eliminar el Precio de producto?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el precio del producto {self.object.product}."
        messages.success(self.request, success_message)
        Notification.objects.create(message=success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
