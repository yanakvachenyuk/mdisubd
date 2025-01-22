from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required

def product_reviews_view(request, product_id):
    # Получаем информацию о продукте
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, description, price
            FROM products
            WHERE id = %s
        """, [product_id])
        product = cursor.fetchone()


    # Если POST-запрос — добавляем отзыв
    if request.method == 'POST' and 'user_id' in request.session:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        user_id = request.session['user_id']

        # Проверка валидности данных
        if rating and comment:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO reviews (user_id, product_id, rating, comment)
                    VALUES (%s, %s, %s, %s)
                """, [user_id, product_id, rating, comment])

            # Перенаправление для предотвращения повторной отправки формы
            return redirect('product_reviews', product_id=product_id)

    # Получаем все отзывы на продукт
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.rating, r.comment, u.name
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.product_id = %s
        """, [product_id])
        reviews = cursor.fetchall()

    return render(request, 'product_reviews.html', {'product': product, 'reviews': reviews})