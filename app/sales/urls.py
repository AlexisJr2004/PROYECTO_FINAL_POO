from django.urls import path
from app.sales.views import sale
 
app_name = 'sales'
urlpatterns = [
    path('sales/list/', sale.SaleListView.as_view(), name='sales_list'),
    path('sales/create/', sale.SaleCreateView.as_view(), name='sales_create'),
    path('sales/update/<int:pk>/', sale.SaleUpdateView.as_view(), name='sales_update'),
    path('sales/annul/<int:pk>/', sale.SaleAnnulView.as_view(), name='sales_annul'),
    path('sales/delete/<int:pk>/', sale.SaleDeleteView.as_view(), name='sales_delete'),
]
