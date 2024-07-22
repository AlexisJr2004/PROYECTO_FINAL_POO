from django.forms import ModelForm
from django import forms
from app.core.models import Product
from django_select2.forms import Select2Widget, Select2MultipleWidget

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["description", "brand", "cost", "price", "stock", "iva", "expiration_date","line", "categories", "image", "state", "active"]
        error_messages = {
            "description": {
                "unique": "Ya existe un producto con este nombre.",
            }
        }
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese producto",
                    "id": "id_description",
                    "class": "border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "brand": Select2Widget(
                attrs={
                    "id": "id_brand",
                }
            ),
            "cost": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese costo",
                    "id": "id_cost",
                    "class": "border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "id": "id_price",
                    "placeholder": "Ingrese precio",
                    "class": "border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "id": "id_stock",
                    "placeholder": "Ingrese stock",
                    "class": "border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "iva": Select2Widget(
                attrs={
                    "id": "id_iva",
                }
            ),
            "expiration_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "id_expiration_date",
                    "class": "border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "line": Select2Widget(
                attrs={
                    "id": "id_line",
                }
            ),
            "categories": Select2MultipleWidget(
                attrs={
                    "id": "id_categories",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "dropzone-file",
                    "class": "hidden",
                }
            ),
            "state": Select2Widget(
                attrs={
                    "id": "id_state",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "id": "id_active",
                    "class": "checkbox-container border-[#AAA8A8] text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[10px] p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "description": "Nombre",
            "brand": "Marca",
            "cost": "Costo",
            "price": "Precio",
            "stock": "Stock",
            "iva": "Iva",
            "expiration_date": "Vencimiento",
            "line": "Línea",
            "categories": "Categorías",
            "image": "Imagen",
            "state": "Estado",
            "active": "Activo",
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return description.upper()