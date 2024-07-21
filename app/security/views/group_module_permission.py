from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Permission
from app.security.forms.group_module_permission import GroupModulePermissionForm
from app.security.models import GroupModulePermission, Module, Group

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

from app.security.mixins.mixins import (
    CreateViewMixin,
    DeleteViewMixin,
    ListViewMixin,
    PermissionMixin,
    UpdateViewMixin,
)
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.contrib import messages
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "security/group_module_permissions/list.html"
    model = GroupModulePermission
    context_object_name = "group_module_permissions"
    permission_required = "view_group_module_permission"

    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get("q")  # ver
        if q1:
            queryset = queryset.filter(Q(group__name__icontains=q1) | Q(module__name__icontains=q1))
        return queryset.order_by("group__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("security:group_module_permission_create")
        return context
    
class GroupModulePermissionCreateView(CreateView):
    model = GroupModulePermission
    template_name = "security/group_module_permissions/form.html"
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy("security:group_module_permission_list")
    permission_required = "add_group_module_permission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grabar"] = "Grabar GMP"
        context["back_url"] = self.success_url
        return context
    
    def get(self, request, *args, **kwargs):
        group_id = request.GET.get('group_id')
        if group_id:
            group = Group.objects.get(id=group_id)
            modules = Module.objects.all()
            permissions_data = []
            for module in modules:
                module_permissions = Permission.objects.filter(module=module)
                selected_permissions = GroupModulePermission.objects.filter(
                    group=group, module=module
                ).values_list('permissions__id', flat=True)
                permissions_data.append({
                    'module_id': module.id,
                    'module_name': module.name,
                    'permissions': [
                        {
                            'id': perm.id,
                            'name': perm.name,
                            'selected': perm.id in selected_permissions
                        } for perm in module_permissions
                    ]
                })
            return JsonResponse({'permissions_data': permissions_data})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group')
        permission_ids = request.POST.getlist('permissions[]')
        
        group = Group.objects.get(id=group_id)
        
        # Eliminar todos los GroupModulePermission existentes para este grupo
        GroupModulePermission.objects.filter(group=group).delete()
        
        # Crear nuevos GroupModulePermission
        for permission_id in permission_ids:
            permission = Permission.objects.get(id=permission_id)
            # Buscar el módulo que contiene este permiso
            module = Module.objects.filter(permissions=permission).first()
            if module:
                gmp, created = GroupModulePermission.objects.get_or_create(
                    group=group,
                    module=module
                )
                gmp.permissions.add(permission)
        
        messages.success(request, "GMP creado con éxito.")
        
        # Obtener la URL de éxito
        success_url = reverse('security:group_module_permission_list')
        
        return JsonResponse({
            'success': True,
            'redirect_url': success_url
        })
        
class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = "security/delete.html"
    success_url = reverse_lazy("security:group_module_permission_list")
    permission_required = "delete_group_module_permission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Módulo"
        context["name"] = f"¿Desea Eliminar los permisos del GMP: {self.object.group}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente los permisos del GMP {self.object.group}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)

