from django.db import connection
from django.shortcuts import redirect,render
from django.contrib import messages

def add_to_cart_view(request):
    if request.method == 'POST' and 'user_id' in request.session:
        product_id = int(request.POST.get('product_id'))
        user_id = request.session['user_id']  # ID текущего пользователя
        quantity = 1  # Добавляем всегда 1 товар

        with connection.cursor() as cursor:
            cursor.execute("CALL add_product_to_cart(%s, %s, %s)", [user_id, product_id, quantity])

        return redirect('clothing_catalog')
    else:
        return redirect('login')


def cart_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']

    # Fetch cart products from the database using a stored procedure
    with connection.cursor() as cursor:
        cursor.execute("SELECT product_id, name, price, quantity FROM fetch_cart_products(%s)", [user_id])
        cart_products = cursor.fetchall()

    return render(request, 'cart.html', {'cart_products': cart_products})

def update_cart_item_view(request, product_id, action):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    with connection.cursor() as cursor:
        if action == 'increase':
            cursor.execute("""
                UPDATE cart_products 
                SET quantity = quantity + 1 
                WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s) AND product_id = %s
            """, [user_id, product_id])
        elif action == 'decrease':
            cursor.execute("""
                UPDATE cart_products 
                SET quantity = GREATEST(quantity - 1, 1) 
                WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s) AND product_id = %s
            """, [user_id, product_id])

    return redirect('cart')

def remove_from_cart_view(request, product_id):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM cart_products 
            WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s) AND product_id = %s
        """, [user_id, product_id])

    return redirect('cart')