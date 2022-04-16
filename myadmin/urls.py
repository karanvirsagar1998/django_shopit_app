from django.contrib import admin
from django.urls import path, include
from myadmin import views
from django.conf.urls.static import static
from shopit import settings

urlpatterns = [
    path('', views.dash),
    path('view-all-cats', views.view_all_cats),
    path('add-new-cat', views.add_new_cat),
    path('view-all-sub-cats', views.view_all_sub_cats),
    path('add-new-sub-cat', views.add_new_sub_cat),
    path('edit-category/<str:id>', views.edit_category),
    path('delete-category/<str:id>/<str:param>', views.delete_category),
    path('edit-sub-category/<str:id>', views.edit_sub_category),
    path('delete-sub-category/<str:id>/<str:param>', views.delete_sub_category),
    path('view-all-products', views.view_all_products),
    path('add-new-product/', views.add_new_product),
    path('edit-product/<str:id>', views.edit_product),
    path('delete-product/<str:id>', views.delete_product),
    path('get-products-count-by-week/<int:month>', views.get_products_count_by_week),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
