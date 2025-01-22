from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def admin_manage_categories_view(request):
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

    # Получение всех категорий
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name
            FROM categories
        """)
        categories = cursor.fetchall()

    # Если POST-запрос — добавляем/обновляем/удаляем категорию
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categories (name)
                    VALUES (%s)
                """, [name])


        elif action == 'edit':
            category_id = request.POST.get('category_id')
            name = request.POST.get('name')
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE categories
                    SET name = %s
                    WHERE id = %s
                """, [name, category_id])


        elif action == 'delete':
            category_id = request.POST.get('category_id')
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM categories
                    WHERE id = %s
                """, [category_id])


        return redirect('admin_manage_categories')  # Перезагрузка страницы после действия

    return render(request, 'admin_manage_categories.html', {'categories': categories})
