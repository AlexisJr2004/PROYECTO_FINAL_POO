# app/core/views/notifications.py

from django.shortcuts import render, redirect
from django.contrib import messages
from app.core.models import Notification

from django.http import JsonResponse
from django.template.loader import render_to_string

from app.sales.models import Invoice

def notification_list(request):
    notifications = Notification.objects.all().order_by('-timestamp')
    total_notifications = Notification.objects.count()
    total_sales = Invoice.objects.count()
    html = render_to_string('components/notification_list.html', {
        'notifications': notifications,
    })
    return JsonResponse({
        'html': html,
        'total_notifications': total_notifications,
        'total_sales': total_sales
    })

def clear_notifications(request):
    Notification.objects.all().delete()
    messages.success(request, 'Se han borrado todas las notificaciones.')
    return redirect('/')
