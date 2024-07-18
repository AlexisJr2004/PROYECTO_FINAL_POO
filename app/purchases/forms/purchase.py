from app.purchases.models import Purchase
from django import forms
from django_select2.forms import Select2Widget

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["num_document", "supplier", "issue_date", "subtotal", "iva", "total", "active"]
        widgets = {
            "num_document": forms.NumberInput(
                attrs={
                    "id": "id_num_document",
                    "placeholder": "Ingrese número de documento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "supplier": Select2Widget(
                attrs={
                    "id": "id_supplier",
                }
            ),
            "issue_date": forms.DateInput(
                attrs={
                    "id": "id_issue_date",
                    "type": "date",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                },
                format='%Y-%m-%d'
            ),
            "subtotal": forms.NumberInput(
                attrs={
                    "id": "id_subtotal",
                    "placeholder": "Ingrese subtotal",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "iva": forms.NumberInput(
                attrs={
                    "id": "id_iva_purchase",
                    "placeholder": "Ingrese IVA",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "total": forms.NumberInput(
                attrs={
                    "id": "id_total",
                    "placeholder": "Ingrese total",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "id": "id_active",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "num_document": "Número de documento",
            "supplier": "Proveedor",
            "issue_date": "Fecha de emisión",
            "subtotal": "Subtotal",
            "iva": "IVA",
            "total": "Total",
            "active": "Activo",
        }
        