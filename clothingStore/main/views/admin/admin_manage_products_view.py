from django.shortcuts import render, redirect
from django.db import connection
from main.models import Users, Categories, Products, Suppliers

def admin_manage_products_view(request):
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

    # Получение всех товаров с учетом поставщиков
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.name, p.description, p.price, p.stock, p.category_id, p.supplier_id, s.name as supplier_name
            FROM products p
            LEFT JOIN suppliers s ON p.supplier_id = s.id
        """)
        products = cursor.fetchall()

    # Получение всех категорий и поставщиков
    categories = Categories.objects.all()
    suppliers = Suppliers.objects.all()

    # Если POST-запрос — добавляем/обновляем/удаляем товар
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category')
            supplier_id = request.POST.get('supplier')
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO products (name, description, price, stock, category_id, supplier_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [name, description, price, stock, category_id, supplier_id])
        elif action == 'edit':
            product_id = request.POST.get('product_id')
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category')
            supplier_id = request.POST.get('supplier')
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE products
                    SET name = %s, description = %s, price = %s, stock = %s, category_id = %s, supplier_id = %s
                    WHERE id = %s
                """, [name, description, price, stock, category_id, supplier_id, product_id])
        elif action == 'delete':
            product_id = request.POST.get('product_id')
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM products
                    WHERE id = %s
                """, [product_id])

        return redirect('admin_manage_products')  # Перезагрузка страницы после действия

    return render(request, 'admin_manage_products.html', {'products': products, 'categories': categories, 'suppliers': suppliers})
