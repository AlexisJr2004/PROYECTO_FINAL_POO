from django.conf import settings
from django.urls import path
from app.core import views
from app.core.views import supplier, company, brand, line, category, iva, product, product_price, product_price_detail, payment_method
from app.core.views.invoice_format import invoice_format
from app.core.views.purchase_format import purchase_format

from app.core.views.get_suppliers import get_suppliers
from app.core.views.get_users import get_users
from .views.notifications import notification_list, clear_notifications

from app.core.views.profile_view import ProfileView, UpdateProfileView
from app.core.views.generate_qr import QRCodeGeneratorView, GenerateLoginQRView, QRScannerView
from app.core.views.scaner_face import FacialRecognitionView
from app.core.views.recuperation_email import CustomPasswordResetConfirmView, PasswordResetView

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language
from django.conf.urls.static import static
from django.urls import include

app_name='core' # define un espacio de nombre para la aplicación
urlpatterns = [    
    path('i18n/', include('django.conf.urls.i18n')),
    # URLs de proveedores
    path('supplier/list/', supplier.SupplierListView.as_view() ,name='supplier_list'),
    path('supplier/create/', supplier.SupplierCreateView.as_view(),name='supplier_create'),
    path('supplier/update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name='supplier_update'),
    path('supplier/delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
    # URLs de compañías
    path('company/list/', company.CompanyListView.as_view(),name='company_list'),
    path('company/create/', company.CompanyCreateView.as_view(),name='company_create'),
    path('company/update/<int:pk>/', company.CompanyUpdateView.as_view(),name='company_update'),
    path('company/delete/<int:pk>/', company.CompanyDeleteView.as_view(),name='company_delete'),
    # URLs de marcas
    path('brand/list/', brand.BrandListView.as_view(),name='brand_list'),
    path('brand/create/', brand.BrandCreateView.as_view(),name='brand_create'),
    path('brand/update/<int:pk>/', brand.BrandUpdateView.as_view(),name='brand_update'),
    path('brand/delete/<int:pk>/', brand.BrandDeleteView.as_view(),name='brand_delete'),
    # URLs de líneas
    path('line/list/', line.LineListView.as_view(),name='line_list'),
    path('line/create/', line.LineCreateView.as_view(),name='line_create'),
    path('line/update/<int:pk>/', line.LineUpdateView.as_view(),name='line_update'),
    path('line/delete/<int:pk>/', line.LineDeleteView.as_view(),name='line_delete'),
    # URLs de categorías
    path('category/list/', category.CategoryListView.as_view(),name='category_list'),
    path('category/create/', category.CategoryCreateView.as_view(),name='category_create'),
    path('category/update/<int:pk>/', category.CategoryUpdateView.as_view(),name='category_update'),
    path('category/delete/<int:pk>/', category.CategoryDeleteView.as_view(),name='category_delete'),
    # URLs de IVA
    path('iva/list/', iva.IvaListView.as_view(),name='iva_list'),
    path('iva/create/', iva.IvaCreateView.as_view(),name='iva_create'),
    path('iva/update/<int:pk>/', iva.IvaUpdateView.as_view(),name='iva_update'),
    path('iva/delete/<int:pk>/', iva.IvaDeleteView.as_view(),name='iva_delete'),
    # URLs de productos
    path('product/list/', product.ProductListView.as_view(),name='product_list'),
    path('product/create/', product.ProductCreateView.as_view(),name='product_create'),
    path('product/update/<int:pk>/', product.ProductUpdateView.as_view(),name='product_update'),
    path('product/delete/<int:pk>/', product.ProductDeleteView.as_view(),name='product_delete'),
    # URLs de precios de productos
    path('product/price_list/', product_price.ProductPriceListView.as_view(),name='product_price_list'),
    path('product/price_create/', product_price.ProductPriceCreateView.as_view(),name='product_price_create'),
    path('product/price_update/<int:pk>/', product_price.ProductPriceUpdateView.as_view(),name='product_price_update'),
    path('product/price_delete/<int:pk>/', product_price.ProductPriceDeleteView.as_view(),name='product_price_delete'),
    # URLs de detalles de precios de productos 
    path('product/price_detail_list/', product_price_detail.ProductPriceDetailListView.as_view(),name='product_price_detail_list'),
    path('product/price_detail_create/', product_price_detail.ProductPriceDetailCreateView.as_view(),name='product_price_detail_create'),
    path('product/price_detail_update/<int:pk>/', product_price_detail.ProductPriceDetailUpdateView.as_view(),name='product_price_detail_update'),
    path('product/price_detail_delete/<int:pk>/', product_price_detail.ProductPriceDetailDeleteView.as_view(),name='product_price_detail_delete'),
    # URLs de métodos de pago
    path('payment_method/list/', payment_method.PaymentMethodListView.as_view(),name='payment_method_list'),
    path('payment_method/create/', payment_method.PaymentMethodCreateView.as_view(),name='payment_method_create'),
    path('payment_method/update/<int:pk>/', payment_method.PaymentMethodUpdateView.as_view(),name='payment_method_update'),
    path('payment_method/delete/<int:pk>/', payment_method.PaymentMethodDeleteView.as_view(),name='payment_method_delete'),
    # URLs de Perfil
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    # URLs de QR
    path('generate-qr-page/<int:user_id>/', QRCodeGeneratorView.as_view(), name='generate_qr_page'),
    path('generate-qr/<int:user_id>/', GenerateLoginQRView.as_view(), name='generate_login_qr'),
    path('qr-scanner/', QRScannerView.as_view(), name='qr_scanner_view'),
    # URLs de Reconocimiento Facial
    path('facial-recognition/', FacialRecognitionView.as_view(), name='facial_recognition'),
    # URLs Recuperara Contraseña
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # URLs Fcatura
    path('invoice_format/<int:invoice_id>/', invoice_format, name='invoice_format'),
    path('purchase_format/<int:purchase_id>/', purchase_format, name='purchase_format'),
    # URLs Obtener todos los proveedores
    path('get-suppliers/', get_suppliers, name='get_suppliers'),
    # URLs Obtener todos los usuarios
    path('get_users/', get_users, name='get_users'),
    # URLs Obtener las notificaciones
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/clear/', clear_notifications, name='clear_notifications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
