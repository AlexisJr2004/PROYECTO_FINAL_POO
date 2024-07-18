from django.urls import reverse_lazy
from app.core.forms.payment_method import PaymentMethodForm
from app.core.models import PaymentMethod
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


class PaymentMethodListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/payment_methods/list.html"
    model = PaymentMethod
    context_object_name = "payment_methods"
    permission_required = "view_paymentmethod"

    def get_queryset(self):
        q1 = self.request.GET.get("q")  # ver
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("core:payment_method_create")
        return context


class PaymentMethodCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = PaymentMethod
    template_name = "core/payment_methods/form.html"
    form_class = PaymentMethodForm
    success_url = reverse_lazy("core:payment_method_list")
    permission_required = "add_paymentmethod"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Grabar Método de Pago "
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        payment_method = self.object
        messages.success(self.request, f"Éxito al crear el Método de Pago {payment_method.description}.")
        return response


class PaymentMethodUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = PaymentMethod
    template_name = "core/payment_methods/form.html"
    form_class = PaymentMethodForm
    success_url = reverse_lazy("core:payment_method_list")
    permission_required = "change_paymentmethod"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Actualizar Método de Pago "
        context["back_url"] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        payment_method = self.object
        messages.success(
            self.request, f"Éxito al actualizar el Método de Pago {payment_method.description}."
        )
        return response


class PaymentMethodDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = PaymentMethod
    template_name = "core/delete.html"
    success_url = reverse_lazy("core:payment_method_list")
    permission_required = "delete_paymentmethod"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["grabar"] = "Eliminar Método de Pago "
        context["description"] = f"¿Desea Eliminar el Método de Pago : {self.object.description}?"
        context["back_url"] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = (
            f"Éxito al eliminar lógicamente el Método de Pago {self.object.description}."
        )
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
