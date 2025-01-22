from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from datetime import date

def create_order_view(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Возвращаем объект HttpResponse (редирект)

    user_id = request.session['user_id']

    # Получение товаров из корзины
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT product_id, quantity
            FROM cart_products
            WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s)
        """, [user_id])
        cart_products = cursor.fetchall()

    if not cart_products:

        return redirect('cart')  # Возвращаем объект HttpResponse (редирект)

    # Создание заказа
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO orders (user_id, order_date, status)
            VALUES (%s, %s, %s) RETURNING id
        """, [user_id, date.today(), 'Не оплачен'])
        order_id = cursor.fetchone()[0]

    # Добавление товаров в order_products
    with connection.cursor() as cursor:
        for product_id, quantity in cart_products:
            cursor.execute("""
                CALL add_product_to_order(%s, %s, %s)
            """, [order_id, product_id, quantity])

        # Очистка корзины
        cursor.execute("""
            DELETE FROM cart_products
            WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s)
        """, [user_id])


    return redirect('order_history')  # Возвращаем объект HttpResponse (редирект)

def mark_order_as_paid_view(request, order_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                CALL update_order_status(%s, %s)
            """, [order_id, 'Оплачен'])

    return redirect('order_history')
