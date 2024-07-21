from django.forms import ModelForm
from django import forms
from app.security.models import User


class UserForm(ModelForm):
    latitude = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "id": "id_latitude",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.000001",
            }
        ),
        required=False
    )
    longitude = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "id": "id_longitude",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.000001",
            }
        ),
        required=False
    )
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "dni", "image", "direction", "phone", "latitude", "longitude"]
        error_messages = {
            "username": {
                "unique": "Ya existe un usuario con este nombre.",
            },
            "email": {
                "unique": "Ya existe un usuario con este email.",
            },
            "dni": {
                "unique": "Ya existe un usuario con este dni.",
            }
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese usuario",
                    "id": "id_username",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombres",
                    "id": "id_first_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese apellidos",
                    "id": "id_last_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese email",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dni",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                }
            ),
            "is_staff": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                }
            ),
            "is_superuser": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "dropzone-file",
                    "class": "hidden",
                }
            ),
            "direction": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dirección",
                    "id": "id_direction",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese teléfono",
                    "id": "id_phone",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "username": "Usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Email",
            "is_active": "Activo",
            "is_staff": "Staff",
            "is_superuser": "Superusuario",
            "dni": "Cédula o RUC",
            "image": "Imagen",
            "direction": "Dirección",
            "phone": "Teléfono",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['latitude'].initial = self.instance.latitude
            self.fields['longitude'].initial = self.instance.longitude

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.latitude = self.cleaned_data.get('latitude')
        instance.longitude = self.cleaned_data.get('longitude')
        if commit:
            instance.save()
        return instance