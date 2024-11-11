# Generated by Django 5.1.2 on 2024-11-10 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cupon',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterField(
            model_name='cupon',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=7, verbose_name='Discount Price'),
        ),
        migrations.AlterField(
            model_name='cupon',
            name='minimum_amount',
            field=models.DecimalField(decimal_places=2, default=500.0, max_digits=8, verbose_name='Minimum Purchase Amount'),
        ),
    ]