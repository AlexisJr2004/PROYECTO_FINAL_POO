from django.forms import ModelForm
from django import forms
from app.core.models import Supplier

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "ruc", "address", "phone", "latitude", "longitude", "active", "image"]
        error_messages = {
            "ruc": {
                "unique": "Ya existe un proveedor con este RUC o DNI.",
            },
            "name": {
                "unique": "Ya existe un proveedor con este nombre.",
            },
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del proveedor",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "ruc": forms.TextInput(
                attrs={
                    "placeholder": "RUC o DNI del proveedor",
                    "id": "id_ruc",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Dirección del proveedor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Número celular",
                    "id": "id_phone",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "latitude": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Latitud",
                    "id": "id_latitude",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "longitude": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Longitud",
                    "id": "id_longitude",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "id": "id_active",
                    "class": "checkbox-container shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[10px] p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "dropzone-file",
                    "class": "hidden",
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "ruc": "Ruc o Dni",
            "address": "Dirección",
            "phone": "Celular",
            "latitude": "Latitud",
            "longitude": "Longitud",
            "state": "Estado",
            "image": "Imagen",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
