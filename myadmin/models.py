from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1000, null=True)

    class Meta:
        db_table = "categories"


class SubCategory(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True)
    category_id = models.IntegerField(null=True)
    description = models.TextField(max_length=1000, null=True)

    class Meta:
        db_table = "subcategories"


class Product(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(null=True)
    sub_category_id = models.IntegerField(null=True)  # type of product
    initial_price = models.FloatField(null=True)  # striked one
    discount = models.FloatField(null=True)
    final_price = models.FloatField(null=True)
    color = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='products')
    date_created = models.DateField(null=True, auto_now_add=True)
    sales = models.IntegerField(null=True)

    class Meta:
        db_table = "products"
