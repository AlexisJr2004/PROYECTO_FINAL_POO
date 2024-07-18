
from django.conf import settings
from django.conf.urls.static import static
from app.core import views as core
from app.security import views as security
from django.contrib import admin
from django.urls import path, include
from app.core.views.home import HomeTemplateView
from app.core.views.modulos import ModuloTemplateView
from app.core.views.consultas import ConsultasTemplateView

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('',HomeTemplateView.as_view(), name='home'),
    path('modulos/',ModuloTemplateView.as_view(), name='modulos'),
    path('consultas/',ConsultasTemplateView.as_view(), name='consultas'),
    path('security/', include('app.security.urls', namespace='security')),
    path('core/', include('app.core.urls', namespace='core')),
    path('sale/', include('app.sales.urls', namespace='sale')),
    path('purchase/', include('app.purchases.urls', namespace='purchases')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
