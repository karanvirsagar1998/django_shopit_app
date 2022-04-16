"""shopit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shopit import settings


urlpatterns = [
    path('', include('myadmin.urls')),
    path('admin/', admin.site.urls),
    # for admin panel
    path('myadmin/', include('myadmin.urls')),
    path('view-all-cats/', include('myadmin.urls')),
    path('add-new-cat/', include('myadmin.urls')),
    path('view-all-sub-cats/', include('myadmin.urls')),
    path('add-new-sub-cat/', include('myadmin.urls')),
    path('edit-category/<str:id>', include('myadmin.urls')),
    path('delete-category/<str:id>/<str:param>/', include('myadmin.urls')),
    path('edit-sub-category/<str:id>', include('myadmin.urls')),
    path('delete-sub-category/<str:id>/<str:param>/', include('myadmin.urls')),
    path('view-all-products', include('myadmin.urls')),
    path('add-new-product/', include('myadmin.urls')),
    path('edit-product/<str:id>', include('myadmin.urls')),
    path('delete-product/<str:id>', include('myadmin.urls')),
    path('get-products-count-by-week/<int:month>', include('myadmin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
