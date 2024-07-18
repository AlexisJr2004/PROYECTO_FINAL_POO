
from django.urls import path
from app.purchases.views import purchase
 
app_name='purchases' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('purchases_list/', purchase.PurchaseListView.as_view() ,name='purchases_list'),
    path('purchases_create/', purchase.PurchaseCreateView.as_view(),name='purchases_create'),
    path('purchases_update/<int:pk>/', purchase.PurchaseUpdateView.as_view(),name='purchases_update'),
    path('purchases_annul/<int:pk>/', purchase.PurchaseAnnulView.as_view(),name='purchases_annul'),
    path('purchases_delete/<int:pk>/', purchase.PurchaseDeleteView.as_view(),name='purchases_delete'),
]