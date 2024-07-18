from django.forms import ModelForm
from django import forms
from app.core.models import Iva

class IvaForm(ModelForm):
    class Meta:
        model = Iva
        fields = ["description", "value", "image", "active"]
        error_messages = {
            "description": {
                "unique": "Ya existe un IVA con este nombre.",
            },
            "value": {
                "unique": "Ya existe un IVA con este valor.",
            }
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese detalle del IVA",
                    "id": "id_description",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "value": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese valor del IVA",
                    "id": "id_value",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "id": "id_active",
                    "class": "checkbox-container shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[10px] p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
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
            "description": "Nombre",
            "value": "Valor (%)",
            "image": "Imagen",
            "active": "Activo",
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description.upper()