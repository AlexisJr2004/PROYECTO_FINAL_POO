# Generated by Django 4.2 on 2024-07-14 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(default=1, max_length=100, verbose_name='Correo'),
            preserve_default=False,
        ),
    ]
