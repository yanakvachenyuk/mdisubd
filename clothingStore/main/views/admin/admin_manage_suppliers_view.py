from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def admin_manage_suppliers_view(request):
    # Проверка, авторизован ли пользователь
    if 'user_id' not in request.session:
        return redirect('login')  # Перенаправление на страницу входа, если пользователь не авторизован

    # Получаем user_id из сессии
    user_id = request.session['user_id']

    # Проверяем, что пользователь — администратор
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT is_superuser
            FROM users
            WHERE id = %s
        """, [user_id])
        user = cursor.fetchone()

    if not user or not user[0]:  # Проверяем, существует ли пользователь и является ли он администратором
        return redirect('clothing_catalog')

    # Получение всех поставщиков
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, contact_info
            FROM suppliers
        """)
        suppliers = cursor.fetchall()

    # Если POST-запрос — добавляем/обновляем/удаляем поставщика
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            contact_info = request.POST.get('contact_info')
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO suppliers (name, contact_info)
                    VALUES (%s, %s)
                """, [name, contact_info])

        elif action == 'edit':
            supplier_id = request.POST.get('supplier_id')
            name = request.POST.get('name')
            contact_info = request.POST.get('contact_info')
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE suppliers
                    SET name = %s, contact_info = %s
                    WHERE id = %s
                """, [name, contact_info, supplier_id])


        elif action == 'delete':
            supplier_id = request.POST.get('supplier_id')
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM suppliers
                    WHERE id = %s
                """, [supplier_id])


        return redirect('admin_manage_suppliers')  # Перезагрузка страницы после действия

    return render(request, 'admin_manage_suppliers.html', {'suppliers': suppliers})
