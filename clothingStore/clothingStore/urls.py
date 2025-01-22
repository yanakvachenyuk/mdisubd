"""
URL configuration for clothingStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from main.views.admin.admin_manage_categories_view import admin_manage_categories_view
from main.views.admin.admin_manage_discounts_view import admin_manage_discounts_view
from main.views.admin.admin_manage_products_view import admin_manage_products_view
from main.views.admin.admin_manage_suppliers_view import admin_manage_suppliers_view
from main.views.admin.audit_logs_view import audit_logs_view
from main.views.auth_views import login_view, register_view, logout_view
from main.views.cart.cart_views import add_to_cart_view, cart_view, update_cart_item_view, remove_from_cart_view
from main.views.cloth.catalog_views import *
from main.views.order.create_order_view import mark_order_as_paid_view, create_order_view
from main.views.order.order_history_view import order_history_view
from main.views.review.product_reviews_view import  product_reviews_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', clothing_catalog_view, name='clothing_catalog'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('update_cart_item/<int:product_id>/<str:action>/', update_cart_item_view, name='update_cart_item'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/checkout/', create_order_view, name='create_order'),
    path('orders/', order_history_view, name='order_history'),
    path('orders/<int:order_id>/pay/', mark_order_as_paid_view, name='mark_order_as_paid'),
    path('products/<int:product_id>/reviews/', product_reviews_view, name='product_reviews'),
    path('admin_manage_products/', admin_manage_products_view, name='admin_manage_products'),
    path('admin_manage_categories/', admin_manage_categories_view, name='admin_manage_categories'),
    path('admin_suppliers/', admin_manage_suppliers_view, name='admin_manage_suppliers'),
    path('admin_discounts/', admin_manage_discounts_view, name='admin_manage_discounts'),
    path('admin_logs/', audit_logs_view, name='audit_logs'),
]
