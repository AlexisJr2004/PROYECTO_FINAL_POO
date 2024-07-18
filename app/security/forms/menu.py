from django.forms import ModelForm
from django import forms
from app.security.models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "icon"]
        error_messages = {
            "name": {
                "unique": "Ya existe un menú con este nombre.",
            }
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese menú",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "icon": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese icono",
                    "id": "id_icon",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "icon": "Icono",
        }
        

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()