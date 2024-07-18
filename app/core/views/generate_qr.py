import json
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

import jwt

User = get_user_model()

class QRCodeGeneratorView(LoginRequiredMixin, TemplateView):
    template_name = 'components/generate_qr.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        return context

class GenerateLoginQRView(LoginRequiredMixin, View):
    def generate_unique_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def get(self, request, user_id):
        try:
            token = self.generate_unique_token(user_id)
            qr_data = {
                'type': 'login',
                'token': token
            }
            return JsonResponse({'qr_data': qr_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class QRScannerView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data')
            
            if qr_data['type'] == 'login':
                user = self.verify_token(qr_data['token'])
                if user:
                    login(request, user)
                    return JsonResponse({
                        "success": True, 
                        "message": "Login successful", 
                        "redirect": "/"
                    })
                else:
                    return JsonResponse({"success": False, "message": "Invalid or expired QR code"}, status=400)
            else:
                return JsonResponse({"success": False, "message": "Invalid QR type"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
        except KeyError:
            return JsonResponse({"success": False, "message": "Missing required data in QR code"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            return User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return None
