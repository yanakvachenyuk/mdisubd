from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(CartProducts)
admin.site.register(Carts)
admin.site.register(Orders)
admin.site.register(OrderProducts)
admin.site.register(Suppliers)
admin.site.register(Discounts)
admin.site.register(Reviews)
admin.site.register(Products)
admin.site.register(Payments)
admin.site.register(AuditLogs)



