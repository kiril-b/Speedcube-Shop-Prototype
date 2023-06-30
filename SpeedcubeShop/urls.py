"""
URL configuration for SpeedcubeShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from SpeedcubeShopApp.views import *

urlpatterns = [
    path('', home),
    path('home/', home, name='home'),
    path('home/<str:category>/', items_in_category, name='items_in_category'),
    path('home/<str:category>/<str:item_id>', item_details, name='item_details'),
    path('shopping-cart', shopping_cart, name='shopping_cart'),
    path('shopping-cart/<str:order_item_id>', delete_order_item, name='delete_order_item'),
    path('checkout/', checkout, name='checkout'),
    path('purchase-history/', purchase_history, name='purchase_history'),
    path('items-session/', new_items_session, name='new_items_session'),
    path('items-session/save', save_employee_session, name='save_employee_session'),
    path('delete-item/<str:item_id>', delete_item, name='delete_item'),
    path('add-item/<str:item_type>', enter_new_item, name='enter_new_item'),
    path('submit-item/', submit_item, name='submit_item'),
    #
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
]
