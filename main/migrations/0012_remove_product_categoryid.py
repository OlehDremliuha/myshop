# Generated by Django 4.2.6 on 2025-06-04 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_product_categoryid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categoryId',
        ),
    ]
