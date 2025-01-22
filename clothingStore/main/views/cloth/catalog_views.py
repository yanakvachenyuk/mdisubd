from django.shortcuts import render
from django.db import connection

def clothing_catalog_view(request):
    # Получение параметров категории и поиска из GET-запроса
    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    # Базовый SQL-запрос для выборки продуктов
    query = """
        SELECT 
            p.id, p.name, p.description, p.price, c.name AS category_name, p.stock, 
            s.name AS supplier_name, d.discount_amount, d.start_date, d.end_date
        FROM 
            products p
        LEFT JOIN 
            categories c ON p.category_id = c.id
        LEFT JOIN 
            suppliers s ON p.supplier_id = s.id
        LEFT JOIN 
            discounts d ON p.id = d.product_id
    """
    params = []
    conditions = []

    # Фильтр по категории
    if selected_category:
        conditions.append("c.name = %s")
        params.append(selected_category)

    # Фильтр по поисковому запросу (по названию и описанию)
    if search_query:
        conditions.append("(LOWER(p.name) LIKE %s OR LOWER(p.description) LIKE %s)")
        search_term = f"%{search_query.lower()}%"
        params.extend([search_term, search_term])

    # Добавление условий в запрос, если они есть
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        products = cursor.fetchall()

    # Получение всех категорий для фильтра
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()

    # Подготовка контекста для передачи данных в шаблон
    context = {
        'products': [
            {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'category': row[4],
                'stock': row[5],
                'supplier': row[6],
                'discount': {
                    'amount': row[7],
                    'start_date': row[8],
                    'end_date': row[9],
                    'final_price': round(row[3] * (1 - row[7] / 100), 2) if row[7] else None  # Итоговая цена
                } if row[7] else None
            }
            for row in products
        ],
        'categories': [category[0] for category in categories],
        'selected_category': selected_category,
        'search_query': search_query,
    }

    return render(request, 'clothing_catalog.html', context)
