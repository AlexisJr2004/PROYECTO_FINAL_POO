import os
import cv2
import numpy as np
import json
import base64
from io import BytesIO
from PIL import Image
import socket
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class FacialRecognitionView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            logger.info("Iniciando reconocimiento facial")
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            logger.info(f"Caras detectadas: {len(faces)}")
            logger.info(f"Usuario autenticado: {request.user.is_authenticated}")
            logger.info(f"Sesión ID: {request.session.session_key}")
            
            if len(faces) != 1:
                return JsonResponse({"success": False, "message": "Se debe detectar exactamente una cara"})
            
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))

            for user in User.objects.all():
                logger.info(f"Comparando con usuario: {user.username}")
                if user.image:
                    profile_image_path = os.path.join(settings.MEDIA_ROOT, str(user.image))
                    if not os.path.exists(profile_image_path):
                        logger.warning(f"Imagen de perfil no encontrada para {user.username}: {profile_image_path}")
                        continue
                    profile_image = cv2.imread(profile_image_path, cv2.IMREAD_GRAYSCALE)
                    if profile_image is None:
                        logger.warning(f"No se pudo leer la imagen de perfil para {user.username}")
                        continue
                    profile_image = cv2.resize(profile_image, (100, 100))
                    similarity = self.compare_faces(profile_image, face)
                    logger.info(f"Similitud con {user.username}: {similarity}")
                    if similarity:
                        login(request, user)
                        request.session.save()
                        logger.info(f"Usuario logueado: {user.username}")
                        logger.info(f"Sesión ID después del login: {request.session.session_key}")
                        logger.info(f"Usuario autenticado después del login: {request.user.is_authenticated}")
                        current_site = get_current_site(request)
                        home_url = f"http://{current_site.domain}{reverse('home')}"
                        response_data = {
                            "success": True,
                            "redirect": home_url,
                            "message": f"Bienvenido, {user.username}!",
                            "sessionid": request.session.session_key
                        }
                        logger.info(f"Enviando respuesta: {response_data}")
                        response = JsonResponse(response_data)
                        response.set_cookie('sessionid', request.session.session_key, httponly=True, samesite='Lax')
                        return response
            
            logger.info("No se encontró coincidencia")
            return JsonResponse({"success": False, "message": "No se encontró una coincidencia facial válida"})
        except socket.error as e:
            if isinstance(e, socket.error) and e.errno == 32:  # Broken pipe
                logger.error("Conexión cerrada por el cliente (Broken pipe)")
                return HttpResponse(status=499)  # Código de estado personalizado para "Client Closed Request"
        except Exception as e:
            logger.error(f"Error en reconocimiento facial: {str(e)}", exc_info=True)
            return JsonResponse({"success": False, "message": "Error interno del servidor"}, status=500)

    def compare_faces(self, known_face, unknown_face):
        difference = cv2.absdiff(known_face, unknown_face)
        similarity = 1 - (np.sum(difference) / (100 * 100 * 255))

        threshold = 0.7
        return similarity > threshold