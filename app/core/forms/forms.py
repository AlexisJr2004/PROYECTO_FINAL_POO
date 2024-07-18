from django import forms
from app.core.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateProfileForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'dni', 'phone', 'email', 'image', 
            'address', 'gender', 'date_of_birth', 'latitude', 'longitude'
        ]
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "dropzone-file",
                    "class": "hidden",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            user = self.instance.user
            if user:
                self.fields['first_name'].initial = user.first_name
                self.fields['last_name'].initial = user.last_name
                self.fields['email'].initial = user.email
            self.fields['phone'].initial = self.instance.phone
            self.fields['dni'].initial = self.instance.dni
            self.fields['address'].initial = self.instance.address
            self.fields['gender'].initial = self.instance.gender
            self.fields['date_of_birth'].initial = self.instance.date_of_birth
            self.fields['latitude'].initial = self.instance.latitude
            self.fields['longitude'].initial = self.instance.longitude
