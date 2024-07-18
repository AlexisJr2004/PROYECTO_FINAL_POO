from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from app.security.forms.auth import CustomUserCreationForm 


# # PAGUINACION
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# # ----------------- Perfil -----------------
# def profile(request):
#     data = {"title1": "IC - Perfil",
#             "title2": "Perfil de Usuario"}
#     return render(request, 'core/profile.html', data)

# #  Actualizar perfil 
# def update_profile(request):
#     data = {"title1": "IC - Actualizar Perfil",
#             "title2": "Actualizar Perfil"}
#     if request.method == 'POST':
#         form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
#             return redirect('profile')
#     else:
#         form = CustomUserUpdateForm(instance=request.user)
    
#     return render(request, 'core/update_profile.html', {'form': form, **data})

@login_required
def signout(request):
    logout(request)
    return redirect("home")

# ----------------- Registro -----------------
def signup(request):
    data = {"title1": "IC - Registro", "title2": "Registro de Usuarios"}
    
    if request.method == "GET":
        return render(request, "security/auth/signup.html", {"form": CustomUserCreationForm(), **data})
    else:
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Bienvenido {username}, tu cuenta ha sido creada exitosamente. Inicia sesión para continuar.")
            return redirect("security:auth_login")
        else:
            messages.error(request, "Error al registrar el usuario. Por favor, revisa los datos ingresados.")
            return render(request, "security/auth/signup.html", {"form": form, **data})

# ----------------- Iniciar Sesión -----------------
def signin(request):
    data = {"title1": "IC - Login", "title2": "Inicio de Sesión"}
    
    if request.method == "GET":
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {"form": AuthenticationForm(), "success_messages": success_messages, **data})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("modulos")
            else:
                messages.error(request, "El usuario o la contraseña son incorrectos")
        return render(request, "security/auth/signin.html", {"form": form, "error": "Datos inválidos", **data})

