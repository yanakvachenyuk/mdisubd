from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import LoginForm
from django.contrib.auth.hashers import make_password, check_password


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, password, is_superuser
                    FROM users
                    WHERE email = %s
                """, [email])
                user = cursor.fetchone()

            if user and check_password(password, user[1]):
                request.session['user_id'] = user[0]
                request.session['is_superuser'] = user[2]
                if user[2]:  # Если is_superuser = True
                    return redirect('admin_manage_products')
                else:
                    return redirect('clothing_catalog')

            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})




def logout_view(request):
    del request.session['user_id']  # Удаляет только user_id
    del request.session['is_superuser']  # Удаляет флаг суперпользователя
    return redirect('clothing_catalog')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Проверка на совпадение паролей
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        # Проверка на уникальность пользователя
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", [email])
            existing_user = cursor.fetchone()

            if existing_user:
                messages.error(request, 'Пользователь с такой электронной почтой уже существует.')
                return redirect('register')

            hashed_password = make_password(password)

            # Создаем нового пользователя
            cursor.execute("""
                INSERT INTO users (name, email, password, address, is_superuser)
                VALUES (%s, %s, %s, %s, %s)
            """, [name, email, hashed_password, address, False])

            user_id = cursor.lastrowid


        return redirect('login')

    return render(request, 'register.html')