# Generated by Django 4.2 on 2024-07-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_customer_latitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='latitude',
            field=models.CharField(max_length=100, verbose_name='Latitud'),
        ),
    ]
