# Generated by Django 5.0.4 on 2024-05-28 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_shippingaddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
