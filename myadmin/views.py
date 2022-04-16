from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib import messages
from django.http import JsonResponse
from json import dumps
from myadmin.models import *
from django.core import serializers
from django.db import connection
import calendar
from datetime import datetime


def dash(request):
    return render(request, 'dash.html')


def view_all_cats(request):
    all_cats = Category.objects.raw('select id,name from categories')
    context = {'categories': all_cats}
    return render(request, 'view-all-cats.html', context)


def add_new_cat(request):
    if request.method == 'POST':
        cat_name = request.POST['cat_name']
        cat_desc = request.POST['cat_desc']
        new_cat = Category(name=cat_name, description=cat_desc)
        try:
            new_cat.save()
            success = 1
            return HttpResponse(success)
        except Exception():
            success = 0
            return HttpResponse(success, exc_info=True)
    else:
        return render(request, 'add-new-cat.html')


def edit_category(request, id):
    data = {}
    if request.method == 'POST':
        cat_name = request.POST['cat_name']
        cat_desc = request.POST['cat_desc']
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE categories SET name = '%s', description='%s' WHERE id = '%s'" % (cat_name, cat_desc, id))
        category = Category.objects.raw(
            'select * from categories where id=%s' % id)[0]
        if category:
            data['success'] = 1
            data['id'] = category.id
            data['name'] = category.name
            data['description'] = category.description
        else:
            data['success'] = 0
        return JsonResponse(data)
    else:
        category = Category.objects.raw(
            'select * from categories where id=%s' % id)[0]
        if category:
            data['success'] = 1
            data['id'] = category.id
            data['name'] = category.name
            data['description'] = category.description
        else:
            data['success'] = 0
        return JsonResponse(data)


def delete_category(request, id, param):
    data = {}
    if param != 'delete':
        category = Category.objects.raw(
            'select * from categories where id=%s' % id)[0]
        if category:
            data['success'] = 1
            data['id'] = category.id
            data['name'] = category.name
            data['description'] = category.description
        else:
            data['success'] = 0
        return JsonResponse(data)
    else:
        bool = 0
        cursor = connection.cursor()
        # to show the name of deleted cat to UI
        category = Category.objects.raw(
            'select * from categories where id=%s' % id)[0]
        data['name'] = category.name
        data['id'] = category.id
        # to check if it has any child or not
        is_child_exist = SubCategory.objects.raw(
            'select * from subcategories where category_id=%s' % id)
        if len(is_child_exist) > 0:
            data['message'] = 'Category cannot be deleted because it has children, please contact your Super-Admin for more information.'
        else:
            # delete processing
            bool = cursor.execute(
                "DELETE from categories WHERE id = '%s'" % id)
        if bool:
            data['success'] = 1
        else:
            data['success'] = 0
        return JsonResponse(data)


def view_all_sub_cats(request):
    all_sub_cats = SubCategory.objects.raw(
        'select subcategories.*, categories.name AS parent, categories.id as parentid from subcategories join categories on categories.id = subcategories.category_id')
    context = {'subcategories': all_sub_cats}
    return render(request, 'view-all-sub-cats.html', context)


def add_new_sub_cat(request):
    categories = Category.objects.raw('select id,name from categories')
    if len(categories) > 0:
        context = {'categories': categories}
    else:
        context = {'notice': "Please create a Parent Category first"}
    if request.method == 'POST':
        sub_cat_name = request.POST['sub_cat_name']
        sub_cat_desc = request.POST['sub_cat_desc']
        category_id = int(request.POST['cat_id'])
        new_sub_cat = SubCategory(
            name=sub_cat_name, category_id=category_id, description=sub_cat_desc)
        try:
            new_sub_cat.save()
            success = 1
            return HttpResponse(success)
        except Exception as e:
            success = 0
            return HttpResponse(success, exc_info=True)
    return render(request, 'add-new-sub-cat.html',  context)


def edit_sub_category(request, id):
    data = {}
    if request.method == 'POST':
        subCat = SubCategory()
        subCat = SubCategory.objects.get(id=id)
        subCat.name = request.POST['subCatName']
        subCat.category_id = request.POST['parentID']
        subCat.description = request.POST['subCatDesc']
        subCat.save()
        updatedSubCat = SubCategory.objects.raw(
            'select subcategories.*, categories.name AS parent, categories.id As parentid from subcategories join categories on categories.id = subcategories.category_id where subcategories.id=%s' % id)[0]
        if updatedSubCat:
            data['success'] = 1
            data['id'] = updatedSubCat.id
            data['name'] = updatedSubCat.name
            data['description'] = updatedSubCat.description
            data['parentCat'] = updatedSubCat.parent
            data['parentId'] = updatedSubCat.parentid
        else:
            data['success'] = 0
        return JsonResponse(data)
    else:
        subcategory = SubCategory.objects.raw(
            'select subcategories.*, categories.name AS parent, categories.id as parentid from subcategories join categories on categories.id = subcategories.category_id where subcategories.id=%s' % id)[0]
        categories = Category.objects.raw('select name, id from categories')
        if subcategory:
            data['success'] = 1
            data['id'] = subcategory.id
            data['name'] = subcategory.name
            data['description'] = subcategory.description
            data['parent'] = subcategory.parent
            data['parentid'] = subcategory.parentid
            data['parent_category_id'] = ''
            data['parent_data'] = serializers.serialize('json', categories)
        else:
            data['success'] = 0
        return JsonResponse(data)


def delete_sub_category(request, id, param):
    data = {}
    if param != 'delete':
        subcategories = Category.objects.raw(
            'select * from subcategories where id=%s' % id)[0]
        category = Category.objects.raw(
            'select name, id from categories where id = %s' % subcategories.category_id)[0]
        if subcategories:
            data['success'] = 1
            data['id'] = subcategories.id
            data['name'] = subcategories.name
            data['description'] = subcategories.description
            data['parent_id'] = category.id
            data['parent_name'] = category.name
        else:
            data['success'] = 0
        return JsonResponse(data)
    else:
        bool = 0
        cursor = connection.cursor()
        # to show the name of deleted sub-cat to UI
        subcategories = SubCategory.objects.raw(
            'select * from subcategories where id=%s' % id)[0]
        data['name'] = subcategories.name
        data['id'] = subcategories.id
        # to check if it has any product or not
        is_product_exist = Product.objects.raw(
            'select * from products where sub_category_id=%s' % id)
        if len(is_product_exist) > 0:
            data['message'] = 'Sub Category cannot be deleted because it has been alloted to products, please contact your Super-Admin for more information.'
        else:
            # delete processing
            bool = cursor.execute(
                "DELETE from subcategories WHERE id = '%s'" % id)
        if bool:
            data['success'] = 1
        else:
            data['success'] = 0
        return JsonResponse(data)


def view_all_products(request):
    products = Product.objects.raw(
        "select products.*, subcategories.name as parentname from products join subcategories on products.sub_category_id=subcategories.id order by products.id DESC")
    context = {'products': products}
    return render(request, 'view-all-products.html',  context)


def add_new_product(request):
    # send subcats to add for the new product
    subcategories = SubCategory.objects.all()
    if request.method == 'POST':
        product = Product()
        product.name = request.POST.get('name')
        product.quantity = int(request.POST.get('quantity'))
        product.sub_category_id = request.POST.get('sub_category_id')
        product.initial_price = request.POST.get('initial_price')
        product.discount = request.POST.get('discount')
        product.final_price = request.POST.get('final_price')
        product.color = request.POST.get('color')
        product.description = request.POST.get('description')
        if len(request.FILES) > 0:
            product.image = request.FILES['product_img']
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('/myadmin/view-all-products')
    return render(request, 'add-new-product.html', {'subcategories': subcategories})


def edit_product(request, id):
    id = int(id)
    product = Product()
    product = Product.objects.get(id=id)
    subcategories = SubCategory.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.quantity = int(request.POST.get('quantity'))
        product.sub_category_id = request.POST.get('sub_category_id')
        product.initial_price = request.POST.get('initial_price')
        product.discount = request.POST.get('discount')
        product.final_price = request.POST.get('final_price')
        product.color = request.POST.get('color')
        product.description = request.POST.get('description')
        if len(request.FILES) > 0:
            product.image = request.FILES['product_img']
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('/myadmin/view-all-products')
    else:
        return render(request, "add-new-product.html", {'product': product, 'subcategories': subcategories})


def delete_product(request, id):
    id = int(id)
    product = Product()
    product = Product.objects.filter(id=id).delete()
    return redirect('/myadmin/view-all-products')


def get_products_count_by_week(request, month):
    products = Product.objects.all()
    count = products.count()
    c = calendar.Calendar()
    today = datetime.today()
    if month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        date = datetime(today.year, month, 1)
        monthName = calendar.month_name[month]
    else:
        date = datetime(today.year, today.month, 1)
        monthName = calendar.month_name[today.month]
    c.setfirstweekday(calendar.SUNDAY)
    weeksWithDayNumber = c.monthdayscalendar(date.year, date.month)
    weekNumber = 0
    countProductsInEachWeek = [weekNumber] * 5
    # count products in each week
    for product in products:
        weekNumber = 0
        count = 0
        if product.date_created.month == date.month:
            for week in weeksWithDayNumber:
                if product.date_created.day in week:
                    count += 1
                    countProductsInEachWeek[weekNumber] += count
                weekNumber += 1
    # sum total products in that month
    totalProducts = 0
    for product in countProductsInEachWeek:
        totalProducts += product
    data = {}
    data['success'] = 1
    data['month'] = date.month
    data['monthName'] = monthName
    data['year'] = date.year
    data['totalProducts'] = totalProducts
    data['countProductsInEachWeek'] = countProductsInEachWeek
    return JsonResponse(data)
