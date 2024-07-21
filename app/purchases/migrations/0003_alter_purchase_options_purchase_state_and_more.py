# Generated by Django 4.2 on 2024-07-21 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notification'),
        ('purchases', '0002_alter_purchase_supplier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ('-issue_date',), 'verbose_name': 'Compra de Producto', 'verbose_name_plural': 'Compras de Productos'},
        ),
        migrations.AddField(
            model_name='purchase',
            name='state',
            field=models.CharField(choices=[('F', 'Factura'), ('M', 'Modificada'), ('A', 'Anulada')], default='F', max_length=1, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_suppliers', to='core.supplier', verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Subtotal'),
        ),
    ]
