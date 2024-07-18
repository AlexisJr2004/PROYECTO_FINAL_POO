from django.urls import reverse_lazy
from app.security.forms.menu import MenuForm
from app.security.models import Menu
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


class MenuListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "security/menus/list.html"
    model = Menu
    context_object_name = "menus"
    permission_required = "view_menu"

    def get_queryset(self):
        q1 = self.request.GET.get("q")  # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("security:menu_create")
        return context


class MenuCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Menu
    template_name = "security/menus/form.html"
    form_class = MenuForm
    success_url = reverse_lazy("security:menu_list")
    permission_required = "add_menu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Grabar Menú"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Éxito al crear el Menú {menu.name}.")
        return response


class MenuUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Menu
    template_name = "security/menus/form.html"
    form_class = MenuForm
    success_url = reverse_lazy("security:menu_list")
    permission_required = "change_menu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Actualizar Menú"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(
            self.request, f"Éxito al actualizar el Menú {menu.name}."
        )
        return response


class MenuDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Menu
    template_name = "security/delete.html"
    success_url = reverse_lazy("security:menu_list")
    permission_required = "delete_menu"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Menú"
        context["name"] = f"¿Desea Eliminar el Menú: {self.object.name}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente el Menú {self.object.name}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
