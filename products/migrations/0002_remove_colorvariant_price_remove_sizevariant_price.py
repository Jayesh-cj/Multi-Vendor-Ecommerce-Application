# Generated by Django 5.1.2 on 2024-11-04 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colorvariant',
            name='price',
        ),
        migrations.RemoveField(
            model_name='sizevariant',
            name='price',
        ),
    ]
