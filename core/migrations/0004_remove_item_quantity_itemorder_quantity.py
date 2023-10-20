# Generated by Django 4.2.6 on 2023-10-20 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='itemorder',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]