# Generated by Django 5.1.2 on 2024-11-06 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_options_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_category', to='products.category'),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]