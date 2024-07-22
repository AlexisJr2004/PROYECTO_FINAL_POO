# Generated by Django 4.2 on 2024-07-22 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='brand',
            index=models.Index(fields=['description'], name='core_brand_descrip_5b1a81_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['description'], name='core_produc_descrip_f55423_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name'], name='core_custom_last_na_c56f78_idx'),
        ),
    ]
