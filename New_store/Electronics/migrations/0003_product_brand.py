# Generated by Django 5.0.3 on 2024-04-19 11:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Electronics', '0002_com'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Electronics.com'),
            preserve_default=False,
        ),
    ]
