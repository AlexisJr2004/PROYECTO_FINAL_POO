from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from app.security.forms.group_module_permission import GroupModulePermissionForm
from app.security.models import GroupModulePermission, Module

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
        context["grabar"] = "Grabar Módulo"
        context["back_url"] = self.success_url
        modules = Module.objects.all()
        permissions_by_module = {
            module.id: list(Permission.objects.filter(module=module).values('id', 'content_type__app_label', 'codename', 'name'))
            for module in modules
        }
        context["modules"] = modules
        context["permissions_by_module"] = json.dumps(permissions_by_module)
        context["selected_permissions"] = json.dumps([])
        context["is_update"] = False  
        return context
    
    def post(self, request, *args, **kwargs):
        form_count = int(request.POST.get('form_count', 1))
        success = True
        errors = []

        for i in range(1, form_count + 1):
            form_data = {
                'group': request.POST.get(f'group_{i}'),
                'module': request.POST.get(f'module_{i}'),
                'permissions': [perm.split(':')[0] for perm in request.POST.getlist(f'permissions_{i}[]') if perm.split(':')[1] == 'true']
            }
            form = self.form_class(form_data)
            if form.is_valid():
                group_module_permission = form.save(commit=False)
                group_module_permission.save()
                group_module_permission.permissions.set(form.cleaned_data.get('permissions', []))
            else:
                success = False
                errors.append(form.errors)

        if success:
            messages.success(request, f"Éxito al crear {form_count} GMP.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': errors})

class GroupModulePermissionUpdateView(UpdateView):
    model = GroupModulePermission
    template_name = "security/group_module_permissions/form.html"
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy("security:group_module_permission_list")
    permission_required = "change_groupmodulepermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar Permisos de Grupo de Módulo"
        context["grabar"] = "Actualizar Módulo"
        context["back_url"] = self.success_url
        modules = Module.objects.all()
        permissions_by_module = {
            module.id: list(Permission.objects.filter(module=module).values('id', 'content_type__app_label', 'codename', 'name'))
            for module in modules
        }
        context["modules"] = modules
        context["permissions_by_module"] = json.dumps(permissions_by_module)
        selected_permissions = list(self.object.permissions.values_list('id', flat=True))
        context["selected_permissions"] = json.dumps(selected_permissions)
        context["is_update"] = True
        return context

    def form_valid(self, form):
        try:
            group_module_permission = form.save(commit=False)
            group_module_permission.permissions.clear()
            selected_permissions = form.cleaned_data.get('permissions', [])
            group_module_permission.permissions.add(*selected_permissions)
            group_module_permission.save()
            messages.success(self.request, f"Éxito al actualizar los permisos del GMP {group_module_permission.group}.")
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_data = {
            'group': request.POST.get('group_1'),
            'module': request.POST.get('module_1'),
            'permissions': [perm.split(':')[0] for perm in request.POST.getlist('permissions_1[]') if perm.split(':')[1] == 'true']
        }
        form = self.form_class(form_data, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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

