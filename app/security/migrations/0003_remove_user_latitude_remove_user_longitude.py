# Generated by Django 4.2 on 2024-07-16 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_user_latitude_user_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='user',
            name='longitude',
        ),
    ]
