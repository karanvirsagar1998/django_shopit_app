# Generated by Django 4.0.1 on 2022-02-13 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_alter_categories_description_alter_categories_photo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]
