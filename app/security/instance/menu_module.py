from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest
from app.security.models import GroupModulePermission, User

class MenuModule:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._path = self._request.path
        print(self._request)
    # añade usuario, grupo y menus al diccionario data y a la session       
    def fill(self, data):
        # añade al diccionario el user, date
        data['user'] = self._request.user
        data['date_time'] = date_time = datetime.now()
        data['date_date'] = date_date = datetime.now().date()
        print(data['user'])
        # verifica si esta autentificado 
        if self._request.user.is_authenticated:
            print( data['user'])
            if self._request.method == 'GET':
                # añade al diccionario el listado de grupos
                data['group_list'] = self._request.user.groups.all().order_by('id')
                print("listado de grupos")
                print(data['group_list'])
                # verifica si no existe 'group_id' en la session(por defecto vacio) del request
                if 'group_id' not in self._request.session:
                    # si existe grupos se añade a la session el primer grupo con su id
                    if data['group_list'].exists():
                        self._request.session['group'] = data['group_list'].first()
                        self._request.session['group_id'] = self._request.session[
                            'group'].id
                
                # verifica cambio de grupo si existe un 'gpid' se actualzia la sesion
                # con el nuevo grupo y su id
                if self._request.session.get('group'):
                    group_id = self._request.GET.get('gpid', None)

                    if group_id is not None:
                        self._request.session['group_id'] = group_id
                        self._request.session['group'] = data['group_list'].get(
                            id=group_id)
                    #  se añade al diccionario el group y los menus y submenus del usuario del grupo 
                    group = self._request.session['group']
                    data['group'] = group
                    data['menu_list'] = self.__get_menu_list(data["user"], group)
                   
      
    def __get_menu_list(self, user: User, group: Group):
        # obtiene todos los modulos del grupo
        group_module_permission_list = GroupModulePermission.get_group_module_permission_active_list(group.id).order_by('module__name')
        # obtiene la lista de menus de tal forma que no se repitan debido que un menu
        # tiene varios modulos 
        menu_unicos= group_module_permission_list.order_by('module__menu_id').distinct(
                'module__menu_id',
            )
        # obtiene cada menu con sus submenus o modulos
        menu_list = [self._get_data_menu_list(x, group_module_permission_list)
            for x in menu_unicos]
        return menu_list

    def _get_data_menu_list(
            self,
            group_module_permission: GroupModulePermission,
            group_module_permission_list
    ):
        
        group_module_permissions = group_module_permission_list.filter(
            module__menu_id=group_module_permission.module.menu_id
        )
        return {
            'menu': group_module_permission.module.menu,
            'group_module_permission_list': group_module_permissions,
        }