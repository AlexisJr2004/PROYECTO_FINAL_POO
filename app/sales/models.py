from django.db import models
from django.utils import timezone
from app.core.models import Customer,PaymentMethod, Product
   
class Invoice(models.Model): 
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='invoice_customers',verbose_name='Cliente')
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE,related_name='invoices_payment',verbose_name='Metodo Pago')
    issue_date = models.DateTimeField(verbose_name='Fecha Emision',default=timezone.now)
    subtotal = models.DecimalField(verbose_name='Subtotal',default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(verbose_name='Iva',default=0, max_digits=16, decimal_places=2)
    discount = models.DecimalField(verbose_name='descuento',default=0, max_digits=16, decimal_places=2)
    total = models.DecimalField(verbose_name='Total',default=0, max_digits=16, decimal_places=2)
    payment = models.DecimalField(verbose_name='Pago',default=0, max_digits=16, decimal_places=2)
    change = models.DecimalField(verbose_name='Cambio',default=0, max_digits=16, decimal_places=2)
    state = models.CharField(verbose_name='Estado',max_length=1,choices=(('F','Factura'),('A','Anulada'),('M','Modificada')),default='F')  
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ('-issue_date',)
        indexes = [models.Index(fields=['issue_date']),]
        
    def delete(self, *args, **kwargs):
        self.active = False
        self.state = 'A'  # Actualizar el estado a 'Anulada'
        self.save()
    
    def __str__(self):
        return f"{self.id} - {self.customer.get_full_name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name='detail',verbose_name='Factura')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='InvoiceDetail_products',verbose_name='Producto')
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(default=0, max_digits=10, decimal_places=2)
 
    class Meta:
        verbose_name = "Factura Detalle"
        verbose_name_plural = "Factura Detalles"
                
        def __str__(self):
            return f"{self.product.description}"
        