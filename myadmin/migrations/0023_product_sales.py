# Generated by Django 4.0.1 on 2022-04-09 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0022_alter_product_discount_alter_product_final_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.IntegerField(null=True),
        ),
    ]