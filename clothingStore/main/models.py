from django.db import models

class AuditLogs(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action = models.TextField()
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_logs'


class CartProducts(models.Model):
    cart = models.OneToOneField('Carts', models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart_products'
        unique_together = (('cart', 'product'),)


class Carts(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'carts'


class Categories(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categories'


class Discounts(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'discounts'


class OrderProducts(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_products'
        unique_together = (('order', 'product'),)


class Orders(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    order_date = models.DateField()
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Payments(models.Model):
    order = models.OneToOneField(Orders, models.DO_NOTHING)
    payment_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'payments'


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Suppliers(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
