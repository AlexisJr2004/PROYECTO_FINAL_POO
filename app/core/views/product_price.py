from django.urls import reverse_lazy
from app.core.forms.product_price import ProductPriceForm
from app.core.models import ProductPrice
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


class ProductPriceListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/product_prices/list.html"
    model = ProductPrice
    context_object_name = "product_prices"
    permission_required = "view_product_price"

    def get_queryset(self):
        q1 = self.request.GET.get("q")  # ver
        if q1 is not None:
            self.query.add(Q(product__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Grabar Precio de Producto"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear el precio de producto.")
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
        messages.success(
            self.request, f"Éxito al actualizar el precio de producto."
        )
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
        success_message = (
            f"Éxito al eliminar lógicamente el precio del producto."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
