from django.contrib.auth.forms import UserCreationForm
from app.security.models import User

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni', 'direction', 'phone', 'image')
