from django.conf import settings
from django.urls import path
from app.core import views
from app.core.views import supplier, company, brand, line, category, iva, product, product_price, product_price_detail, payment_method
from app.core.views.invoice_format import invoice_format

from app.core.views.get_suppliers import get_suppliers
from app.core.views.get_users import get_users

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
    path('supplier_list/', supplier.SupplierListView.as_view() ,name='supplier_list'),
    path('supplier_create/', supplier.SupplierCreateView.as_view(),name='supplier_create'),
    path('supplier_update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name='supplier_update'),
    path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
    # URLs de compañías
    path('company_list/', company.CompanyListView.as_view(),name='company_list'),
    path('company_create/', company.CompanyCreateView.as_view(),name='company_create'),
    path('company_update/<int:pk>/', company.CompanyUpdateView.as_view(),name='company_update'),
    path('company_delete/<int:pk>/', company.CompanyDeleteView.as_view(),name='company_delete'),
    # URLs de marcas
    path('brand_list/', brand.BrandListView.as_view(),name='brand_list'),
    path('brand_create/', brand.BrandCreateView.as_view(),name='brand_create'),
    path('brand_update/<int:pk>/', brand.BrandUpdateView.as_view(),name='brand_update'),
    path('brand_delete/<int:pk>/', brand.BrandDeleteView.as_view(),name='brand_delete'),
    # URLs de líneas
    path('line_list/', line.LineListView.as_view(),name='line_list'),
    path('line_create/', line.LineCreateView.as_view(),name='line_create'),
    path('line_update/<int:pk>/', line.LineUpdateView.as_view(),name='line_update'),
    path('line_delete/<int:pk>/', line.LineDeleteView.as_view(),name='line_delete'),
    # URLs de categorías
    path('category_list/', category.CategoryListView.as_view(),name='category_list'),
    path('category_create/', category.CategoryCreateView.as_view(),name='category_create'),
    path('category_update/<int:pk>/', category.CategoryUpdateView.as_view(),name='category_update'),
    path('category_delete/<int:pk>/', category.CategoryDeleteView.as_view(),name='category_delete'),
    # URLs de IVA
    path('iva_list/', iva.IvaListView.as_view(),name='iva_list'),
    path('iva_create/', iva.IvaCreateView.as_view(),name='iva_create'),
    path('iva_update/<int:pk>/', iva.IvaUpdateView.as_view(),name='iva_update'),
    path('iva_delete/<int:pk>/', iva.IvaDeleteView.as_view(),name='iva_delete'),
    # URLs de productos
    path('product_list/', product.ProductListView.as_view(),name='product_list'),
    path('product_create/', product.ProductCreateView.as_view(),name='product_create'),
    path('product_update/<int:pk>/', product.ProductUpdateView.as_view(),name='product_update'),
    path('product_delete/<int:pk>/', product.ProductDeleteView.as_view(),name='product_delete'),
    # URLs de precios de productos
    path('product_price_list/', product_price.ProductPriceListView.as_view(),name='product_price_list'),
    path('product_price_create/', product_price.ProductPriceCreateView.as_view(),name='product_price_create'),
    path('product_price_update/<int:pk>/', product_price.ProductPriceUpdateView.as_view(),name='product_price_update'),
    path('product_price_delete/<int:pk>/', product_price.ProductPriceDeleteView.as_view(),name='product_price_delete'),
    # URLs de detalles de precios de productos 
    path('product_price_detail_list/', product_price_detail.ProductPriceDetailListView.as_view(),name='product_price_detail_list'),
    path('product_price_detail_create/', product_price_detail.ProductPriceDetailCreateView.as_view(),name='product_price_detail_create'),
    path('product_price_detail_update/<int:pk>/', product_price_detail.ProductPriceDetailUpdateView.as_view(),name='product_price_detail_update'),
    path('product_price_detail_delete/<int:pk>/', product_price_detail.ProductPriceDetailDeleteView.as_view(),name='product_price_detail_delete'),
    # URLs de métodos de pago
    path('payment_method_list/', payment_method.PaymentMethodListView.as_view(),name='payment_method_list'),
    path('payment_method_create/', payment_method.PaymentMethodCreateView.as_view(),name='payment_method_create'),
    path('payment_method_update/<int:pk>/', payment_method.PaymentMethodUpdateView.as_view(),name='payment_method_update'),
    path('payment_method_delete/<int:pk>/', payment_method.PaymentMethodDeleteView.as_view(),name='payment_method_delete'),
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
    # URLs Obtener todos los proveedores
    path('get-suppliers/', get_suppliers, name='get_suppliers'),
    # URLs Obtener todos los usuarios
    path('get_users/', get_users, name='get_users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
