# Generated by Django 4.2.6 on 2023-10-27 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_order_billing_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='same_billing_address',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='save_info',
        ),
    ]
