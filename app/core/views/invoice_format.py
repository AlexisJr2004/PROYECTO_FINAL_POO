from django.shortcuts import get_object_or_404, render

from app.sales.models import Invoice


def invoice_format(request, invoice_id):
    invoice = get_object_or_404(Invoice.objects.select_related('customer', 'payment_method').prefetch_related('detail__product'), id=invoice_id)
    
    # Calcula el porcentaje de IVA
    if invoice.subtotal > 0:
        iva_percentage = (invoice.iva / invoice.subtotal) * 100
    else:
        iva_percentage = 0
    
    context = {
        'invoice': invoice,
        'title1': 'Factura',
        'title2': 'Detalle de la Factura',
        'iva_percentage': round(iva_percentage, 2)
    }
    return render(request, 'components/invoice_format.html', context)

from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    return value + timedelta(days=days)