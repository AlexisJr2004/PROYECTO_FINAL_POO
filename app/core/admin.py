from django.contrib import admin

from app.core.models import Supplier, Company, Brand, Line, Category, Iva, Product, ProductPrice, ProductPriceDetail, PaymentMethod, Customer

admin.site.register(Supplier)
admin.site.register(Company)
admin.site.register(Brand)
admin.site.register(Line)
admin.site.register(Category)
admin.site.register(Iva)
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(ProductPriceDetail)
admin.site.register(PaymentMethod)
admin.site.register(Customer)