from django.views.generic import TemplateView
from app.core.models import Company, Supplier, Customer, Notification
from app.sales.models import Invoice

class HomeTemplateView(TemplateView):
    template_name = 'components/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "IC - Inicio"
        context["title2"] = "Corporacion el Rosado"
        
        # Cargar notificaciones
        notifications = Notification.objects.all().order_by('-timestamp')
        
        companies = Company.objects.all()
        customers = Customer.objects.all()
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
