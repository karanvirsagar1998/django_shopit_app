# Generated by Django 4.0.2 on 2022-03-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0020_alter_product_description_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
