import os
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from app.core.models import Customer, Notification
from app.core.forms.forms import UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import default_storage

User = get_user_model()

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'components/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        customer = get_object_or_404(Customer, user=user)
        
        context.update({
            "user": user,
            "customer": customer,
            "title1": "Perfil de Usuario",
            "title2": "Información del Perfil del Usuario"
        })
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = UpdateProfileForm
    template_name = 'components/update_profile.html'
    success_url = reverse_lazy('core:profile')

    def get_object(self, queryset=None):
        user = self.request.user
        customer, created = Customer.objects.get_or_create(user=user)
        return customer

    def form_valid(self, form):
        user = self.request.user
        customer = self.get_object()

        # Actualizar los campos del usuario
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        # Actualizar los campos del customer
        customer.phone = form.cleaned_data['phone']
        customer.dni = form.cleaned_data['dni']
        customer.address = form.cleaned_data['address']
        customer.gender = form.cleaned_data['gender']
        customer.date_of_birth = form.cleaned_data['date_of_birth']
        customer.latitude = form.cleaned_data['latitude']
        customer.longitude = form.cleaned_data['longitude']

        new_image = self.request.FILES.get('image')
        if new_image:
            # Si hay una imagen existente, elimínala
            if customer.image:
                if os.path.isfile(customer.image.path):
                    os.remove(customer.image.path)
            
            # Guarda la nueva imagen
            file_name = default_storage.save(f'customers/{new_image.name}', new_image)
            customer.image = file_name

        customer.save()

        # Actualizar contraseña si se proporciona
        current_password = form.cleaned_data.get('current_password')
        new_password1 = form.cleaned_data.get('new_password1')
        new_password2 = form.cleaned_data.get('new_password2')

        if current_password and new_password1 and new_password2:
            if user.check_password(current_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(self.request, user)  # Mantener la sesión activa
                    success_message = 'Contraseña actualizada con éxito.'
                    messages.success(self.request, success_message)
                    Notification.objects.create(message=success_message)
                else:
                    error_message = 'Las nuevas contraseñas no coinciden.'
                    messages.error(self.request, error_message)
                    Notification.objects.create(message=error_message)
            else:
                error_message = 'La contraseña actual es incorrecta.'
                messages.error(self.request, error_message)
                Notification.objects.create(message=error_message)

        success_message = 'Perfil actualizado con éxito.'
        messages.success(self.request, success_message)
        Notification.objects.create(message=success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = "Actualizar Perfil"
        context['title2'] = "Actualiza tu información personal"
        return context
