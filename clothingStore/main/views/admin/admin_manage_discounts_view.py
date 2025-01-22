from django.shortcuts import render, redirect
from django.db import connection

def admin_manage_discounts_view(request):
    # Получение данных о скидках с присоединением продуктов
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT d.id, d.discount_amount, d.start_date, d.end_date, COALESCE(p.name, 'Нет данных') AS product_name, d.product_id
            FROM discounts d
            LEFT JOIN products p ON d.product_id = p.id
        """)
        columns = [col[0] for col in cursor.description]
        discounts = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Получение списка всех продуктов
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM products")
        products = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            product_id = request.POST.get('product')
            discount_amount = request.POST.get('discount_amount')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Добавление новой скидки
            if action == "add":
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CALL add_discount(%s, %s, %s, %s)
                    """, [product_id, discount_amount, start_date, end_date])

        elif action == 'edit':
            discount_id = request.POST.get('discount_id')
            product_id = request.POST.get('product')
            discount_amount = request.POST.get('discount_amount')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Обновление скидки
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE discounts
                    SET product_id = %s, discount_amount = %s, start_date = %s, end_date = %s
                    WHERE id = %s
                """, [product_id, discount_amount, start_date, end_date, discount_id])

        elif action == 'delete':
            discount_id = request.POST.get('discount_id')

            # Удаление скидки
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM discounts WHERE id = %s", [discount_id])

        return redirect('admin_manage_discounts')

    return render(request, 'admin_manage_discounts.html', {
        'discounts': discounts,
        'products': products
    })
