# Generated by Django 5.0.3 on 2024-12-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0003_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='ord_status',
            field=models.BooleanField(default=False),
        ),
    ]
