
from django.db.models import Q
from app.security.instance.group_permission import GroupPermission
from app.security.instance.menu_module import MenuModule
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

# configuracion de contexto generico y permisos de botones
class ListViewMixin(object):
    query = None
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        self.query = Q()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = f'IG - {self.model._meta.verbose_name_plural}'
        context['title2'] = f'Consulta de {self.model._meta.verbose_name_plural}'
        # añade los permisos del grupo activo(add_pais, view_ciudad)
        # print("estoy en el mixing..")
        # print(self.request.session.get('group_id'))
        context['permissions'] = self._get_permission_dict_of_group()
        # crear la data y la session con los menus y modulos del usuario 
        MenuModule(self.request).fill(context)
        return context

    def _get_permission_dict_of_group(self):
        print("user:=",self.request.user)
        return GroupPermission.get_permission_dict_of_group(self.request.user)

class CreateViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'IG - {self.model._meta.verbose_name}'
        context['title2'] = f'Creación de {self.model._meta.verbose_name_plural}'
        context['permissions'] = self._get_permission_dict_of_group()
        MenuModule(self.request).fill(context)
        return context

    def _get_permission_dict_of_group(self):
        return GroupPermission.get_permission_dict_of_group(self.request.user)

class UpdateViewMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'IG - {self.model._meta.verbose_name_plural}'
        context['title2'] = f'Actualización de {self.model._meta.verbose_name_plural}'
        context['permissions'] = self._get_permission_dict_of_group()
        MenuModule(self.request).fill(context)
        
        return context

    def _get_permission_dict_of_group(self):
        return GroupPermission.get_permission_dict_of_group(self.request.user)
    
class DeleteViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("entro al deleteMixin")
        context['title'] = f'IG - {self.model._meta.verbose_name_plural}'
        context['permissions'] = self._get_permission_dict_of_group()
        MenuModule(self.request).fill(context)
        return context

    def _get_permission_dict_of_group(self):
        return GroupPermission.get_permission_dict_of_group(self.request.user)
    
         
# Permisos de urls o modulos
class PermissionMixin(object):
    permission_required = ''
    print("Entrando a permisos mixin...")
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user.set_group_session()

            if 'group_id' not in request.session:
                return redirect('home')

            if user.is_superuser:
                return super().get(request, *args, **kwargs)

            group = user.get_group_session()
            permissions = self._get_permissions_to_validate()

            if not permissions.__len__():
                return super().get(request, *args, **kwargs)

            if not group.groupmodulepermission_set.filter(
                    permissions__codename__in=permissions
            ).exists():
                print("No tengo permisos...")
                messages.error(request, 'No tiene permiso para ingresar a este módulo')
                return redirect('home')

            return super().get(request, *args, **kwargs)

        except Exception as ex:
            messages.error(
                request,
                'A ocurrido un error al ingresar al modulo, error para el admin es : {}'.format(ex))

        if request.user.is_authenticated:
            return redirect('home')

        return redirect('security:auth_login')

    def _get_permissions_to_validate(self):

        if self.permission_required == '':
            return ()

        if isinstance(self.permission_required, str):
            return self.permission_required,

        return tuple(self.permission_required)     
    
