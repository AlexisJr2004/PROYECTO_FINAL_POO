from django.forms import ModelForm
from django import forms
from app.core.models import Company

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["dni", "name", "address", "representative", "landline", "website", "logo", "email", "establishment_code", "emission_point_code", "authorization_number", "taxpayer_type", "required_to_keep_accounting", "economic_activity_code"]
        error_messages = {
            "name": {
                "unique": "Ya existe una compañía con este nombre.",
            },
            "website": {
                "unique": "Ya existe una compañía con este sitio web.",
            },
            "email": {
                "unique": "Ya existe una compañía con este correo electrónico.",
            },
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese compañía",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese RUC o DNI",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dirección de la compañía",
                    "id": "id_address",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "representative": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese representante de la compañía",
                    "id": "id_representative",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "landline": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese teléfono fijo de la compañía",
                    "id": "id_landline",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "website": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese sitio web de la compañía",
                    "id": "id_website",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "logo": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "dropzone-file",
                    "class": "hidden",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese correo electrónico de la compañía",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "establishment_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de establecimiento",
                    "id": "id_establishment_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "emission_point_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de punto de emisión",
                    "id": "id_emission_point_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "authorization_number": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese número de autorización",
                    "id": "id_authorization_number",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "taxpayer_type": forms.Select(
                attrs={
                    "id": "id_taxpayer_type",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "required_to_keep_accounting": forms.CheckboxInput(
                attrs={
                    "id": "id_required_to_keep_accounting",
                    "class": "checkbox-container shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-[10px] p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "economic_activity_code": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese código de actividad económica",
                    "id": "id_economic_activity_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "dni": "RUC",
            "name": "Nombre",
            "address": "Dirección",
            "representative": "Representante",
            "landline": "Teléfono Fijo",
            "website": "Sitio Web",
            "logo": "Logo",
            "email": "Correo Electrónico",
            "establishment_code": "Código de Establecimiento",
            "emission_point_code": "Código de Punto de Emisión",
            "authorization_number": "Número de Autorización",
            "taxpayer_type": "Tipo de Contribuyente",
            "required_to_keep_accounting": "Requiere Llevar Contabilidad",
            "economic_activity_code": "Código Actividad Económica",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()