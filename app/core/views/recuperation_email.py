from django.core.mail import send_mail
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.templatetags.static import static
from django.views import View

User = get_user_model()

class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'components/password_reset.html', {'title1': 'Recuperar Contraseña'})
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            
            # Generar token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir el enlace de restablecimiento
            reset_link = request.build_absolute_uri(
                reverse('core:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Obtener la URL de la imagen estática
            logo_url = 'https://www.iguanadigital.com.ec/images/Logo/iguana-digital-logo_mesa-de-trabajo-1-copia.png'
            web_url = 'http://127.0.0.1:8000/'  # Reemplaza con tu URL real de la aplicación

            # Configurar el asunto y el mensaje del correo
            subject = 'Restablecimiento de Contraseña - IGUANA CORP'
            message = format_html(
                """
                <html>
                    <body>
                        <div style="text-align: center;">
                            <img src="{logo_url}" alt="IGUANA CORP Logo" style="width: 150px; height: auto;">
                        </div>
                        <br>
                        Estimado usuario,
                        <br><br>
                        Hemos recibido una solicitud para restablecer la contraseña de su cuenta.
                        <br><br>
                        Para proceder con el restablecimiento, por favor haga clic en el siguiente enlace:
                        <br><br>
                        <a href="{reset_link}" style="color: blue;">{reset_link}</a>
                        <br><br>
                        Si usted no solicitó este cambio, puede ignorar este correo. Su contraseña actual seguirá siendo válida.
                        <br><br>
                        Este enlace expirará en 24 horas por razones de seguridad.
                        <br><br>
                        Si tiene alguna pregunta o necesita asistencia adicional, no dude en contactarnos.
                        <br><br>
                        Atentamente,
                        <br>
                        El equipo de <strong><a href="{web_url}" style="color: black;">IGUANA CORP</a></strong>.
                        <br><br>
                        Nota: Este es un correo automático, por favor no responda a esta dirección.
                        </body>
                </html>
                """,
                logo_url=logo_url,
                reset_link=reset_link,
                web_url=web_url
            )

            from_email = 'noreply@tuempresa.com'
            recipient_list = [email]

            # Enviar el correo
            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message)
            
            messages.success(request, f'Se ha enviado un enlace para restablecer tu contraseña a {email}.')
            return redirect(reverse('security:auth_login'))
        except User.DoesNotExist:
            messages.error(request, 'El correo no se encuentra registrado.')
        
        return render(request, 'components/password_reset.html', {'title1': 'Recuperar Contraseña'})

# Añade estas nuevas vistas
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'components/password_reset_confirm.html'
    success_url = reverse_lazy('security:auth_login')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña ha sido cambiada exitosamente.')
        return super().form_valid(form)
