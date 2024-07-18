from django.http import JsonResponse
from app.core.models import Supplier

def get_suppliers(request):
    suppliers = Supplier.objects.filter(active=True).values('name', 'latitude', 'longitude')
    return JsonResponse(list(suppliers), safe=False)

