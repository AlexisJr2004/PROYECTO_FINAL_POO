# Generated by Django 4.2 on 2024-07-17 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_remove_user_latitude_remove_user_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
