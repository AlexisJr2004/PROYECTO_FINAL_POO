from django.urls import path
from app.security.views import auth, menu, module, group_module_permission, user
app_name = "security"
# security
urlpatterns = [
    # auth
    path('auth/login/',auth.signin,name="auth_login"),
    path('auth/signup/',auth.signup,name='auth_signup'),
    path('auth/logout/',auth.signout,name='auth_logout'),
    # menu
    path('menu/list/',menu.MenuListView.as_view(),name='menu_list'),
    path('menu/create/',menu.MenuCreateView.as_view(),name='menu_create'),
    path('menu/update/<int:pk>/',menu.MenuUpdateView.as_view(),name='menu_update'),
    path('menu/delete/<int:pk>/',menu.MenuDeleteView.as_view(),name='menu_delete'),
    # module
    path('module/list/',module.ModuleListView.as_view(),name='module_list'),
    path('module/create/',module.ModuleCreateView.as_view(),name='module_create'),
    path('module/update/<int:pk>/',module.ModuleUpdateView.as_view(),name='module_update'),
    path('module/delete/<int:pk>/',module.ModuleDeleteView.as_view(),name='module_delete'),
    # group_module_permission
    path('group_module_permission/list/', group_module_permission.GroupModulePermissionListView.as_view(), name='group_module_permission_list'),
    path('group_module_permission/create/', group_module_permission.GroupModulePermissionCreateView.as_view(), name='group_module_permission_create'),
    path('group_module_permission/delete/<int:pk>/', group_module_permission.GroupModulePermissionDeleteView.as_view(), name='group_module_permission_delete'),
    # user 
    path('user/list/',user.UserListView.as_view(),name='user_list'),
    path('user/create/',user.UserCreateView.as_view(),name='user_create'),
    path('user/update/<int:pk>/',user.UserUpdateView.as_view(),name='user_update'),
    path('user/delete/<int:pk>/',user.UserDeleteView.as_view(),name='user_delete'),
]
