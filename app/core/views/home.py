from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView
from app.core.models import Company, Brand, Supplier, Line, Category, Product, Customer, PaymentMethod, Iva
from app.security.models import User
from app.sales.models import Invoice
from django.db.models import Q

class HomeTemplateView(TemplateView):
    template_name = 'components/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"title1": "IC - Inicio",
            "title2": "Corporacion el Rosado"}
        
        companies = Company.objects.all()
        brands = Brand.objects.filter(active=True)
        lines = Line.objects.filter(active=True)
        customers = Customer.objects.all()
        categories = Category.objects.filter(active=True)
        products = Product.objects.filter(active=True)
        payment_methods = PaymentMethod.objects.filter(active=True)
        users_admin = User.objects.filter(Q(is_superuser=True) & Q(is_staff=True) & Q(is_active=True))
        suppliers = Supplier.objects.filter(active=True)
        
        context['companies'] = companies
        context['total_companies'] = companies.count()
        
        context['suppliers'] = suppliers
        context['total_suppliers'] = suppliers.count()
        
        context['customers'] = customers
        context['total_customers'] = customers.count()
        
        total_sales = Invoice.objects.count()
        context['total_sales'] = total_sales

        return context