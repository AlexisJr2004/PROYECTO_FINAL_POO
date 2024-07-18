from django.urls import reverse_lazy
from app.security.forms.module import ModuleForm
from app.security.models import Module
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
from django.contrib.auth.models import Permission
from django.core.serializers import serialize
import json

class ModuleListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "security/modules/list.html"
    model = Module
    context_object_name = "modules"
    permission_required = "view_module"

    def get_queryset(self):
        q1 = self.request.GET.get("q")  # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("security:module_create")
        return context

class ModuleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Module
    template_name = "security/modules/form.html"
    form_class = ModuleForm
    success_url = reverse_lazy("security:module_list")
    permission_required = "add_module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grabar"] = "Grabar Módulo"
        context["back_url"] = self.success_url
        context["permissions_json"] = json.dumps(list(Permission.objects.values('id', 'name', 'codename', 'content_type__app_label')))
        context["selected_permissions_json"] = json.dumps([])  # No hay permisos seleccionados al crear
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(self.request, f"Éxito al crear el Módulo {module.name}.")
        return response


class ModuleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Module
    template_name = "security/modules/form.html"
    form_class = ModuleForm
    success_url = reverse_lazy("security:module_list")
    permission_required = "change_module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grabar"] = "Actualizar Módulo"
        context["back_url"] = self.success_url
        context["permissions_json"] = json.dumps(list(Permission.objects.values('id', 'name', 'codename', 'content_type__app_label')))
        context["selected_permissions_json"] = json.dumps(list(self.object.permissions.values_list('id', flat=True)))
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        module = self.object
        messages.success(
            self.request, f"Éxito al actualizar el Módulo {module.name}."
        )
        return response

class ModuleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Module
    template_name = "security/delete.html"
    success_url = reverse_lazy("security:module_list")
    permission_required = "delete_module"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Módulo"
        context["name"] = f"¿Desea Eliminar el Módulo: {self.object.name}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente el Módulo {self.object.name}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
