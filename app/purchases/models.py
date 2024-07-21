from django.db import models
from django.utils import timezone
from app.core.models import Product, Supplier

class Purchase(models.Model):
    STATE_CHOICES = [
        ('F', 'Factura'),
        ('M', 'Modificada'),
        ('A', 'Anulada')
    ]
    
    num_document = models.CharField(verbose_name='NumDocumento', max_length=50, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_suppliers', verbose_name='Supplier')
    issue_date = models.DateTimeField(verbose_name='Fecha Emision', default=timezone.now, db_index=True)
    subtotal = models.DecimalField(verbose_name='Subtotal', default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(verbose_name='Iva', default=0, max_digits=16, decimal_places=2)
    total = models.DecimalField(verbose_name='Total', default=0, max_digits=16, decimal_places=2)
    active = models.BooleanField(verbose_name='Activo', default=True)
    state = models.CharField(verbose_name='Estado', max_length=1, choices=STATE_CHOICES, default='F')
   
    class Meta:
        verbose_name = 'Compra de Producto'
        verbose_name_plural = 'Compras de Productos'
        ordering = ('-issue_date',)

    def annul(self):
        self.active = False
        self.state = 'A'
        self.save()

    def __str__(self):
        return "{} - {:%d-%m-%Y}".format(self.num_document, self.issue_date)

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='purchase_detail', verbose_name='Compra')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_products')
    quantify = models.DecimalField(verbose_name='Cantidad', default=0, max_digits=8, decimal_places=2)
    cost = models.DecimalField(verbose_name='Costo', default=0, max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(verbose_name='Subtotal', default=0, max_digits=16, decimal_places=2)
    iva = models.DecimalField(verbose_name='Iva', default=0, max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de la Compra'
        ordering = ('id',)

    def __str__(self):
        return "{} - {} ".format(self.purchase, self.product.description)
