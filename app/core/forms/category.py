from django.forms import ModelForm
from django import forms
from app.core.models import Category

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["description", "image", "active"]
        error_messages = {
            "description": {
                "unique": "Ya existe una categoría con este nombre.",
            }
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese categoría",
                    "id": "id_description",
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
            "image": "Imagen",
            "active": "Activo",
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description.upper()