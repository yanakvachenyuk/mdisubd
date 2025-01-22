SELECT * FROM users;

SELECT * FROM discounts;

SELECT * FROM order_products;

SELECT * FROM orders;

SELECT * FROM products;

SELECT * FROM payments;

SELECT * FROM audit_logs;

SELECT * FROM users WHERE email = 'ivanov@example.com';

SELECT * FROM categories;

SELECT * FROM products WHERE price < 50;

SELECT * FROM products ORDER BY price ASC;

-- Поиск пользователя по email при входе:
SELECT * FROM users WHERE email = 'ivanov@example.com' AND password = 'password123';

-- Фильтрация пользователей, у которых статус суперпользователя:
SELECT * FROM users WHERE is_superuser = TRUE;

-- Фильтрация товаров по категории:
SELECT * FROM products
WHERE category_id = 1;

-- Поиск товара по названию:
SELECT * FROM products
WHERE name LIKE '%костюм%';

-- Поиск товаров по описанию:
SELECT * FROM products
WHERE description LIKE '%Удобные%';

SELECT id, name, description, price, category_id 
FROM products 
WHERE (category_id = 1 )
  AND (name LIKE '% Джи%' 
       OR description LIKE '%Удо%');


-- Просмотр истории заказов пользователя:
SELECT * FROM orders WHERE user_id = 1;

-- Просмотр статуса оплаты заказа:
SELECT payment_status FROM payments WHERE order_id = 1;

-- Просмотр журнала действий пользователя:
SELECT * FROM audit_logs WHERE user_id = 1;

-- Просмотр всех товаров от конкретного поставщика:
SELECT * FROM products WHERE supplier_id = 1;

-- Фильтрация заказов по статусу:
SELECT * FROM orders WHERE status = 'В процессе';




------------- 4 лр --------------

-- Запросы с несколькими условиями:
-- Фильтрация товаров по разным критериям (например, цена, наличие скидки и категория)

SELECT * 
FROM products 
WHERE price BETWEEN 10 AND 60 
  AND category_id = 1;
  

SELECT p.* 
FROM products p
JOIN discounts d ON p.id = d.product_id
WHERE p.price BETWEEN 0 AND 100  
  AND d.start_date <= CURRENT_DATE  
  AND d.end_date >= CURRENT_DATE  
  AND p.category_id IN (1, 2, 3, 4);  



-- Запросы с вложенными конструкциями:
-- Товары, которые заказываются вместе с другими.

SELECT p.name AS ProductName
FROM products p
WHERE p.id IN (
    SELECT op.product_id -- продукты, которые находятся в заказах с продуктом id=6
    FROM order_products op
    WHERE op.order_id IN (
        SELECT op2.order_id  -- заказы, которые содержат продукт с id=6
        FROM order_products op2
        WHERE op2.product_id = 6
    )
);


-- Прочие сложные выборки, необходимые в проекте:
-- Товаров с отзывами выше определенного рейтинга.

SELECT * 
FROM products 
WHERE id IN (
    SELECT product_id 
    FROM reviews 
    WHERE rating >= 4);





-- Получение представлений с JOIN-запросами:
-- INNER JOIN:
-- Получение списка товаров и их категорий.

SELECT products.name, categories.name 
FROM products 
INNER JOIN categories ON products.category_id = categories.id;


-- LEFT JOIN (LEFT OUTER JOIN):
-- Для получения всех категорий, даже если в них нет товаров.

SELECT categories.name AS category, products.name AS product 
FROM categories 
LEFT JOIN products ON categories.id = products.category_id;


-- FULL JOIN:
-- Полная информация обо всех продуктах и категориях, даже если некоторые данные отсутствуют.

SELECT categories.name AS category, products.name AS product 
FROM categories 
FULL JOIN products ON categories.id = products.category_id;




-- Сгруппированные данные:
-- GROUP BY + агрегирующие функции:
-- Средняя цена товаров в каждой категории.

SELECT category_id, AVG(price) AS AvgPrice 
FROM products 
GROUP BY category_id;


-- Подсчет среднего рейтинга каждого товара.

SELECT product_id, AVG(rating) AS AvgRating
FROM reviews
GROUP BY product_id;


-- PARTITION BY + оконные функции:
-- Для получения ранжированных данных по ценам товаров в каждой категории.

SELECT name, category_id, price, 
RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS Rank
FROM products;


-- HAVING:
--Чтобы выбрать только те категории, где средняя цена превышает определенное значение.
-----------добавить средний рейтинг превышает---------
SELECT category_id, AVG(price) AS AvgPrice 
FROM products 
GROUP BY category_id 
HAVING AVG(price) > 40;


--UNION:
-- История заказов и действий для указанного пользователя

SELECT id AS entity_id, user_id, 'Order' AS entity_type, status AS details, order_date AS date
FROM orders
WHERE user_id = 1

UNION

SELECT id AS entity_id, user_id, 'AuditLog' AS entity_type, action AS details, timestamp AS date
FROM audit_logs
WHERE user_id = 1
ORDER BY date DESC;





--Сложные операции с данными:
--EXISTS:
--все категории, в которых есть хотя бы один товар

SELECT id, name 
FROM categories 
WHERE EXISTS (
    SELECT 1 
    FROM products 
    WHERE products.category_id = categories.id
);


-- товары, для которых есть активные скидки:

SELECT id, name, price 
FROM products 
WHERE EXISTS (
    SELECT 1 
    FROM discounts 
    WHERE discounts.product_id = products.id 
      AND discounts.start_date <= CURRENT_DATE
      AND discounts.end_date >= CURRENT_DATE
);




--INSERT INTO SELECT:
--Вставка популярных товаров в отдельную таблицу для анализа.

INSERT INTO PopularProducts (ProductId, ProductName)
SELECT ProductId, ProductName 
FROM Products 
WHERE ProductId IN (SELECT ProductId 
                    FROM OrderItems 
                    GROUP BY ProductId 
                    HAVING COUNT(*) > 10);



-- CASE:
--Сортировка заказов по статусу с CASE в ORDER BY
--сначала выведет заказы со статусом «Отправлен», затем — «В процессе», и в конце — «Отменен».
--Здесь CASE используется для упорядочивания, присваивая каждому статусу числовое значение, которое определяет порядок.

SELECT id, user_id, status, order_date
FROM orders
ORDER BY 
    CASE 
        WHEN status = 'Отправлен' THEN 1
        WHEN status = 'В процессе' THEN 2
        ELSE 3
    END;



--каждый отзыв будет классифицирован как «Excellent», «Good» или «Poor» на основе его рейтинга.

SELECT product_id, id AS review_id, rating,
    CASE 
        WHEN rating = 5 THEN 'Excellent'
        WHEN rating >= 3 THEN 'Good'
        ELSE 'Poor'
    END AS RatingDescription
FROM reviews;







-- EXPLAIN:
-- Чтобы проверить эффективность сложных запросов, используется команда EXPLAIN.

EXPLAIN SELECT * 
FROM products 
INNER JOIN order_products ON products.id = order_products.product_id 
WHERE order_products.quantity > 5;


--drop
CREATE OR REPLACE FUNCTION update_payment_status_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE payments
    SET status = 'Ожидает обработки'
    WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_payment_status_on_insert
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION update_payment_status_on_insert();

------------------------------------------

--drop
CREATE OR REPLACE PROCEDURE get_user_orders(user_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    SELECT * FROM orders WHERE user_id = user_id;
END;
$$;
