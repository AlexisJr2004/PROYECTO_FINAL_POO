from django.urls import reverse_lazy
from app.core.forms.brand import BrandForm
from app.core.models import Brand
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


class BrandListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/brands/list.html"
    model = Brand
    context_object_name = "brands"
    permission_required = "view_brand"

    def get_queryset(self):
        q1 = self.request.GET.get("q")  # ver
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("core:brand_create")
        return context


class BrandCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Brand
    template_name = "core/brands/form.html"
    form_class = BrandForm
    success_url = reverse_lazy("core:brand_list")
    permission_required = "add_brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Grabar Marca"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        brand = self.object
        messages.success(self.request, f"Éxito al crear la marca {brand.description}.")
        return response


class BrandUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Brand
    template_name = "core/brands/form.html"
    form_class = BrandForm
    success_url = reverse_lazy("core:brand_list")
    permission_required = "change_brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Actualizar Marca"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        brand = self.object
        messages.success(
            self.request, f"Éxito al actualizar la marca {brand.description}."
        )
        return response


class BrandDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Brand
    template_name = "core/delete.html"
    success_url = reverse_lazy("core:brand_list")
    permission_required = "delete_brand"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Marca"
        context["description"] = f"¿Desea Eliminar la Marca: {self.object.description}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente la marca {self.object.description}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
