from django.shortcuts import render, redirect
from django.db import connection

def order_history_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Получаем список заказов с адресом доставки из таблицы users
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.id, o.order_date, o.status, o.total_amount, u.address
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.user_id = %s
        """, [user_id])
        orders = cursor.fetchall()

    # Преобразуем заказы в удобный для шаблона формат
    order_list = []
    with connection.cursor() as cursor:
        for order in orders:
            order_id, order_date, status, total_amount, address = order

            # Получаем список товаров для каждого заказа
            cursor.execute("""
                SELECT p.name, op.quantity, p.price, (op.quantity * p.price) AS total_price
                FROM order_products op
                JOIN products p ON op.product_id = p.id
                WHERE op.order_id = %s
            """, [order_id])
            products = cursor.fetchall()

            # Формируем структуру для одного заказа
            order_list.append({
                'id': order_id,
                'date': order_date,
                'status': status,
                'address': address,
                'total': total_amount,
                'products': products,
            })

    # Передаем данные в шаблон
    return render(request, 'order_history.html', {'orders': order_list})
