import os
from django.core.mail import send_mail
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.templatetags.static import static
from django.views import View
from app.core.models import Notification

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
            logo_url = 'https://imgur.com/a/n5jHFrn'
            web_url = 'http://127.0.0.1:8000/'  # Reemplaza con tu URL real de la aplicación

            # Configurar el asunto y el mensaje del correo
            subject = 'Restablecimiento de Contraseña - IGUANA CORP'

            message = format_html(
                """
                <!DOCTYPE html>
                <html lang="es">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Restablecimiento de Contraseña - IGUANA CORP</title>
                        <style>
                            @keyframes fadeIn {{
                                from {{ opacity: 0; }}
                                to {{ opacity: 1; }}
                            }}
                            @keyframes slideIn {{
                                from {{ transform: translateY(-20px); opacity: 0; }}
                                to {{ transform: translateY(0); opacity: 1; }}
                            }}
                            body {{
                                font-family: 'Arial', sans-serif;
                                line-height: 1.6;
                                color: #333333;
                                background-color: #f4f4f4;
                                margin: 0;
                                padding: 0;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 20px auto;
                                background-color: #ffffff;
                                border-radius: 8px;
                                overflow: hidden;
                                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                                animation: fadeIn 0.5s ease-out;
                            }}
                            .header {{
                                background-color: #0056b3;
                                color: #ffffff;
                                text-align: center;
                                padding: 20px;
                            }}
                            .logo {{
                                width: 80px;
                                height: auto;
                            }}
                            .company-name {{
                                font-size: 28px;
                                font-weight: bold;
                                margin-top: 10px;
                            }}
                            .content {{
                                padding: 30px;
                                animation: slideIn 0.5s ease-out;
                            }}
                            h2 {{
                                color: #0056b3;
                                border-bottom: 2px solid #0056b3;
                                padding-bottom: 10px;
                            }}
                            .button {{
                                display: inline-block;
                                padding: 12px 24px;
                                background-color: #0056b3;
                                color: #ffffff !important;
                                text-decoration: none;
                                border-radius: 5px;
                                font-weight: bold;
                                margin-top: 20px;
                                transition: background-color 0.3s ease;
                            }}
                            .button:hover {{
                                background-color: #003d82;
                            }}
                            .footer {{
                                background-color: #f8f8f8;
                                text-align: center;
                                padding: 20px;
                                font-size: 14px;
                                color: #666666;
                            }}
                            .contact-info {{
                                margin-top: 20px;
                                border-top: 1px solid #dddddd;
                                padding-top: 20px;
                            }}
                            .contact-info h3 {{
                                color: #0056b3;
                                font-size: 18px;
                                margin-bottom: 15px;
                            }}
                            .contact-item {{
                                display: flex;
                                align-items: flex-start;
                                margin-bottom: 15px;
                            }}
                            .contact-item svg {{
                                flex-shrink: 0;
                                margin-right: 10px;
                                margin-top: 3px;
                            }}
                            .contact-item a, .contact-item span {{
                                color: #333333;
                                text-decoration: none;
                            }}
                            .contact-item a:hover {{
                                color: #0056b3;
                                text-decoration: underline;
                            }}
                            @media only screen and (max-width: 600px) {{
                                .container {{
                                    width: 100%;
                                    margin: 0;
                                    border-radius: 0;
                                }}
                            }}
                            .contact-container {{
                                display: flex;
                                justify-content: space-around;
                                text-align: center;
                            }}
                            .contact-section {{
                                flex: 1;
                                margin: 0 10px;
                            }}
                            .section-icon {{
                                font-size: 24px;
                                margin-bottom: 10px;
                            }}
                            .contact-item {{
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                            }}
                            .contact-item svg {{
                                margin-bottom: 5px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <div class="company-name">Iguana Corp</div>
                            </div>
                            <div class="content">
                                <h2>Restablecimiento de Contraseña</h2>
                                <p>Estimado usuario,</p>
                                <p>Hemos recibido una solicitud para restablecer la contraseña de su cuenta.</p>
                                <p>Para proceder con el restablecimiento, por favor haga clic en el siguiente botón:</p>
                                <a href="{reset_link}" class="button">Restablecer Contraseña</a>
                                <p>Si usted no solicitó este cambio, puede ignorar este correo. Su contraseña actual seguirá siendo válida.</p>
                                <p>Este enlace expirará en 24 horas por razones de seguridad.</p>
                                <p>Si tiene alguna pregunta o necesita asistencia adicional, no dude en contactarnos.</p>
                                <p>Atentamente,<br><strong>El equipo de Iguana Corp</strong></p>
                            </div>
                            <div style="text-align: center;" class="footer">
                                <p>Este es un correo automático, por favor no responda a esta dirección.</p>
                                <div class="contact-container">
                                    <div class="contact-section">
                                        <div class="section-icon">
                                            <svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 3h18v18H3z" fill="none"/><path d="M20 4H4v14h16V4zM4 2C2.9 2 2 2.9 2 4v14c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H4zm0 4l8 5 8-5H4zm0 2l8 5 8-5v6l-8 5-8-5V8z"/></svg>
                                        </div>
                                        <div class="contact-item">
                                            <a href="mailto:support@iguanacorp.com">support@iguanacorp.com</a>
                                        </div>
                                    </div>
                                    <div class="contact-section">
                                        <div class="section-icon">
                                            <svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3.6c4.02 0 7.41 3.05 7.93 7h-2.08c-.42-2.22-2.26-3.9-4.59-4.33V5.61c2.97.35 5.26 2.67 5.67 5.66h-1.74C15.1 9.41 13.66 8.24 12 8.24V5.61zm-1.5 5.49H5.07C5.5 7.95 8.53 5.6 12 5.6v2.62c-1.66 0-3.1 1.17-3.43 2.77zm1.5 5.78c-4.02 0-7.41-3.05-7.93-7h2.08c.42 2.22 2.26 3.9 4.59 4.33v2.77c-2.97-.35-5.26-2.67-5.67-5.66h1.74C8.9 14.59 10.34 15.76 12 15.76v2.63zm1.5-3.37H18.93c-.43 2.42-3.46 4.77-7.93 4.77v-2.62c1.66 0 3.1-1.17 3.43-2.77z"/></svg>
                                        </div>
                                        <div class="contact-item">
                                            <a href="https://www.google.com/maps/place/UNEMI+-+Universidad+Estatal+de+Milagro/@-2.149223,-79.60552,17z/data=!3m1!4b1!4m5!3m4!1s0x902d1edc7183f1e5:0x77206e08da0eb158!8m2!3d-2.1492284!4d-79.6033313" target="_blank">
                                                Dirección Google Maps
                                            </a>
                                        </div>
                                    </div>
                                    <div class="contact-section">
                                        <div class="section-icon">
                                            <svg width="24" height="24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 3h18v18H3z" fill="none"/><path d="M16.59 5.41L12 10l-4.59-4.59L6 6l6 6 6-6zM5 19v-2h14v2H5z"/></svg>
                                        </div>
                                        <div class="contact-item">
                                            <a href="https://iguanacorp.com" target="_blank">www.iguanacorp.com</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </body>
                </html>
                """,
                reset_link=reset_link
            )


            from_email = 'noreply@tuempresa.com'
            recipient_list = [email]

            # Enviar el correo
            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message)
            
            success_message = f'Se ha enviado un enlace para restablecer tu contraseña a {email}.'
            messages.success(request, success_message)
            Notification.objects.create(message=success_message)
            return redirect(reverse('security:auth_login'))
        except User.DoesNotExist:
            error_message = 'El correo no se encuentra registrado.'
            messages.error(request, error_message)
            Notification.objects.create(message=error_message)
        
        return render(request, 'components/password_reset.html', {'title1': 'Recuperar Contraseña'})

# Añade estas nuevas vistas
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'components/password_reset_confirm.html'
    success_url = reverse_lazy('security:auth_login')

    def form_valid(self, form):
        success_message = 'Tu contraseña ha sido cambiada exitosamente.'
        messages.success(self.request, success_message)
        Notification.objects.create(message=success_message)
        return super().form_valid(form)
