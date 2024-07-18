from django.http import JsonResponse
from app.security.models import User

def get_users(request):
    users = User.objects.filter(is_active=True).values('username', 'latitude', 'longitude')
    return JsonResponse(list(users), safe=False)