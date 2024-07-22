import datetime
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.db.models import F 
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from proy_sales.utils import phone_regex, valida_cedula, valida_numero_flotante_positivo, valida_numero_entero_positivo
import os

        
class Company(models.Model):
    dni = models.CharField(verbose_name='RUC', max_length=13, blank=True, null=True)
    name = models.CharField(verbose_name='Empresa', max_length=50)
    address = models.CharField(verbose_name='Dirección', max_length=200, blank=True, null=True)
    representative = models.CharField(verbose_name='Responsable', max_length=50, blank=True, null=True)
    landline = models.CharField(verbose_name='Teléfono Fijo', max_length=10, blank=True, null=True)
    website = models.URLField(verbose_name='Sitio Web', max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo Electrónico', max_length=100, blank=True, null=True)
    logo = models.ImageField(verbose_name='Logo', upload_to='company/', blank=True, null=True)
    # Campos adicionales para la factura del SRI
    establishment_code = models.CharField(
        verbose_name='Código de Establecimiento', max_length=3, blank=True, null=True, default='001',
        help_text='Código de tres dígitos asignado al establecimiento por el SRI. Para empresas sin sucursales, usar "001".'
    )
    emission_point_code = models.CharField(
        verbose_name='Código de Punto de Emisión', max_length=3, blank=True, null=True, default='001',
        help_text='Código de tres dígitos del punto de emisión. Para empresas con un solo punto de emisión, usar "001".'
    )
    authorization_number = models.CharField(
        verbose_name='Número de Autorización', max_length=49, blank=True, null=True, default='12345678901234567890123456789012345678901234567890',
        help_text='Número de autorización otorgado por el SRI.'
    )
    taxpayer_type = models.CharField(
        verbose_name='Tipo de Contribuyente', max_length=50, blank=True, null=True, default='ordinary',
        choices=[
            ('special', 'Contribuyente Especial'),
            ('ordinary', 'Contribuyente Ordinario')
        ], 
        help_text='Tipo de contribuyente según clasificación del SRI.'
    )
    required_to_keep_accounting = models.BooleanField(
        verbose_name='Obligado a Llevar Contabilidad', default=True, 
        help_text='Indica si la empresa está obligada a llevar contabilidad.'
    )
    
    economic_activity_code = models.CharField(
        verbose_name='Código de Actividad Económica', max_length=10, blank=True, null=True, default='1234567890',
        help_text='Código de la actividad económica según el SRI.'
    )
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    description = models.CharField(verbose_name='Articulo', max_length=100,unique=True)
    image = models.ImageField(verbose_name='Imagen',upload_to='brands/', blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
  
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['description']
        indexes = [models.Index(fields=['description'])]

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
    
    def __str__(self):
        return self.description

class Line(models.Model):
    description = models.CharField(verbose_name='Linea', max_length=100,unique=True)
    image = models.ImageField(verbose_name='Imagen',upload_to='lines/', blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
     
    class Meta:
        verbose_name = 'Línea'
        verbose_name_plural = 'Líneas'
        ordering = ['description']
      
    def delete(self, *args, **kwargs):
        self.active = False
        self.save() 
    
    def __str__(self):
        return self.description

class Category(models.Model):
    description = models.CharField(verbose_name='Categoría', max_length=100,unique=True)
    image = models.ImageField(verbose_name='Imagen',upload_to='categories/', blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
  
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['description']
      
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
          
    def __str__(self):
        return self.description

class Iva(models.Model):
    description = models.CharField(verbose_name='Iva', max_length=100,unique=True)
    value = models.DecimalField(verbose_name='Porcentaje(%)',max_digits=6, decimal_places=2)
    image = models.ImageField(verbose_name='Imagen',upload_to='ivas/', blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    class Meta:
        verbose_name = 'Iva'
        verbose_name_plural = 'Ivas'
        ordering = ('id',)
           
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
          
    def __str__(self):
        return self.description

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)
    
class Product(models.Model):
    description = models.CharField(verbose_name='Nombre',max_length=100,unique=True,db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='product_brands', verbose_name='Marca')
    cost=models.DecimalField(verbose_name='Costo Producto',max_digits=10,decimal_places=2,default=Decimal('0.0'))
    price = models.DecimalField(verbose_name='Precio',max_digits=10, decimal_places=2,validators=[valida_numero_flotante_positivo])
    stock = models.IntegerField(verbose_name='Costo',default=100,validators=[valida_numero_entero_positivo])
    iva = models.ForeignKey(Iva,on_delete=models.PROTECT, related_name='product_iva', verbose_name='Iva')
    expiration_date = models.DateTimeField(verbose_name='Caducidad', default=timezone.now)
    line = models.ForeignKey(Line, on_delete=models.PROTECT,related_name='product_lines', verbose_name='Linea')
    categories = models.ManyToManyField('Category',related_name="products_categories", verbose_name='Categoria')
    image = models.ImageField(verbose_name='Imagen',upload_to='products/', blank=True, null=True)
    state = models.CharField(verbose_name='Activo',max_length=1, choices=(('A','Activo'),('B','De Baja')), default = 'A')
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    objects = models.Manager()  # Manager predeterminado
    active_products = ActiveProductManager()  
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['description']
        indexes = [models.Index(fields=['description']),]

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
        
    def __str__(self):
        return self.description

    
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',args=[self.id])
    
    @property
    def get_categories(self):
        return " - ".join([c.description for c in self.categories.all().order_by('description')])
    
    def reduce_stock(self,quantity):
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= quantity
        self.save()
    
    def increase_stock(self,quantity):
        self.stock += quantity
        self.save()
    
    @staticmethod
    def update_stock(self,id,quantity):
         Product.objects.filter(pk=id).update(stock=F('stock') - quantity)

from django.db import models
from app.core.models import Product, Line, Category

class ProductPrice(models.Model):
    TYPE_INCREMENT_CHOICES = [
        ('P', 'Porcentaje'),
        ('V', 'Valor'),
    ]
    
    STATE_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices', verbose_name='Producto')
    line = models.ForeignKey(Line, on_delete=models.PROTECT, related_name='product_prices', verbose_name='Línea')
    category = models.ManyToManyField(Category, related_name='product_prices', verbose_name='Categoría')
    type_increment = models.CharField(max_length=1, choices=TYPE_INCREMENT_CHOICES, verbose_name='Tipo de incremento')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    issue_date = models.DateField(verbose_name='Fecha de emisión')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    active = models.BooleanField(default=True, verbose_name='Activo')
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='A', verbose_name='Estado')

    class Meta:
        verbose_name = 'Precio de Producto'
        verbose_name_plural = 'Precios de Productos'
        ordering = ['-issue_date', 'product']

    def __str__(self):
        return f"{self.product} - {self.value} ({self.get_type_increment_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.active and self.state == 'A':
            current_price = self.product.price
            if self.type_increment == 'V':
                new_price = current_price + self.value
            else:  # Porcentaje
                increment = current_price * (self.value / Decimal('100'))
                new_price = current_price + increment
            self.product.price = new_price
            self.product.save()
            

class ProductPriceDetail(models.Model):
    productpreci = models.ForeignKey(ProductPrice, on_delete=models.PROTECT,related_name='productPrice_detail',verbose_name='Producto Precio detalle')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='price_detail',verbose_name='Producto Precio detalle')
    increment = models.DecimalField(verbose_name='Incremento',default=0, max_digits=11, decimal_places=2)
    old_price = models.DecimalField(verbose_name='Precio anterior', default=0, max_digits=11, decimal_places=2)
    issue_date = models.DateTimeField(verbose_name='Fecha Emision',default=timezone.now)
    observation = models.TextField(blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    @property
    def new_price(self):
        return self.old_price+self.increment
    
    class Meta:
        verbose_name = 'Producto Precios Detalle'
        verbose_name_plural = 'Productos Precios Detalles'
        ordering = ('id',)
 
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
        
    def __str__(self):
        return "{} - {}".format(self.product,self.new_price)

class Customer(models.Model): 
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    dni = models.CharField(verbose_name='Dni',max_length=13, unique=True, blank=True, null=True)
    first_name = models.CharField(verbose_name='Nombres',max_length=50)
    last_name = models.CharField(verbose_name='Apellidos',max_length=50)
    address = models.TextField(verbose_name='Dirección',blank=True, null=True)
    gender = models.CharField(verbose_name='Sexo',max_length=1, choices=(('M','Masculino'),('F','Femenino')), default='M')
    date_of_birth = models.DateField(verbose_name='Fecha Nacimiento',blank=True, null=True)
    phone = models.CharField(verbose_name='Telefono',max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name='Correo',max_length=100)
    latitude = models.CharField(verbose_name='Latitud',max_length=100)
    longitude = models.CharField(verbose_name='Longitud',max_length=100)
    image = models.ImageField(verbose_name='Foto',upload_to='customers/',blank=True,null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
     
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['last_name']
        indexes = [models.Index(fields=['last_name']),]

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.upper()
        if self.last_name:
            self.last_name = self.last_name.upper()
        super(Customer, self).save(*args, **kwargs)
    
    @property
    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/usuario_anonimo.png'
        
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class PaymentMethod(models.Model):
    description = models.CharField(verbose_name='Metodo de Pago',max_length=100)
    image = models.ImageField(verbose_name='Foto',upload_to='paymentmethods/',blank=True,null=True)
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    class Meta:
        verbose_name = 'Metodo de Pago'
        verbose_name_plural = 'Metodo de Pagos'
        ordering = ['description']
               
    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
        
    def __str__(self):
        return self.description
 
class Supplier(models.Model):
    name = models.CharField(verbose_name='Nombres', max_length=100, unique=True)
    ruc = models.CharField(verbose_name='Dni', max_length=10, validators=[valida_cedula], unique=True)
    image = models.ImageField(verbose_name='Imagen', upload_to='suppliers/', blank=True, null=True)
    phone = models.CharField(verbose_name='Telefono', max_length=10, validators=[phone_regex])
    address = models.CharField(verbose_name='Direccion', max_length=200)
    latitude = models.CharField(verbose_name='Latitud',max_length=100)
    longitude = models.CharField(verbose_name='Longitud',max_length=100)
    active = models.BooleanField(verbose_name='Activo',default=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def delete(self, *args, **kwargs):
        self.active = False
        self.save()
        
    def __str__(self):
        return self.name
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/usuario_anonimo.png'
 
class Notification(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message