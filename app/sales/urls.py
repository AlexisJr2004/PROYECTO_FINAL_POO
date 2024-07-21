from django.urls import path
from app.sales.views import sale
 
app_name = 'sales'
urlpatterns = [
    path('sales_list/', sale.SaleListView.as_view(), name='sales_list'),
    path('sales_create/', sale.SaleCreateView.as_view(), name='sales_create'),
    path('sales_update/<int:pk>/', sale.SaleUpdateView.as_view(), name='sales_update'),
    path('sales_annul/<int:pk>/', sale.SaleAnnulView.as_view(), name='sales_annul'),
    path('sales_delete/<int:pk>/', sale.SaleDeleteView.as_view(), name='sales_delete'),
]
