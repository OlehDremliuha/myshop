# Generated by Django 4.2.6 on 2025-06-04 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_product_categoryid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categoryId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
            preserve_default=False,
        ),
    ]
