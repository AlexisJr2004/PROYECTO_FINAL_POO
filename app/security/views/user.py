from django.urls import reverse_lazy
from app.security.forms.user import UserForm
from app.security.models import User
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


class UserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "security/users/list.html"
    model = User
    context_object_name = "users"
    permission_required = "view_user"

    def get_queryset(self):
        q1 = self.request.GET.get("q")
        queryset = self.model.objects.select_related('customer').all()
        if q1 is not None:
            queryset = queryset.filter(
                Q(username__icontains=q1) |
                Q(customer__dni__icontains=q1) |
                Q(first_name__icontains=q1) |
                Q(last_name__icontains=q1) |
                Q(customer__address__icontains=q1)
            )
        return queryset.order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("security:user_create")
        return context


class UserCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = User
    template_name = "security/users/form.html"
    form_class = UserForm
    success_url = reverse_lazy("security:user_list")
    permission_required = "add_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Grabar Usuario"
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Éxito al crear al usuario {user.username}.")
        return response


class UserUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    template_name = "security/users/form.html"
    form_class = UserForm
    success_url = reverse_lazy("security:user_list")
    permission_required = "change_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Actualizar Usuario"
        context["back_url"] = self.success_url
        return context


    def form_valid(self, form):
        customer = form.save(commit=False)
        user = customer.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        customer.save()
        return super().form_valid(form)


class UserDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = User
    template_name = "security/delete.html"
    success_url = reverse_lazy("security:user_list")
    permission_required = "delete_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Usuario"
        context["name"] = f"¿Desea Eliminar al Usuario: {self.object.group}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente al Usuario {self.object.username}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
