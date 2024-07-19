from django.shortcuts import get_object_or_404, render

from app.purchases.models import Purchase, PurchaseDetail
from django.db.models import Prefetch

def purchase_format(request, purchase_id):
    purchase = get_object_or_404(
        Purchase.objects.select_related('supplier').prefetch_related(
            Prefetch('purchase_detail', queryset=PurchaseDetail.objects.select_related('product'))
        ),
        id=purchase_id
    )
    
    context = {
        'purchase': purchase,
        'title1': 'Factura',
        'title2': 'Detalle de la Factura',
    }
    return render(request, 'components/purchase_format.html', context)
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    return value + timedelta(days=days)