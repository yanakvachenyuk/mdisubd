-- Редактирование товара (изменение цены и количества на складе):
UPDATE products
SET price = 89.99, stock = 40
WHERE id = 1;

-- Изменение названия категории):
UPDATE categories
SET name = 'Спортивная обувь'
WHERE id = 2;

-- Изменение количества товара в корзине:
UPDATE cart_products
SET quantity = 3
WHERE cart_id = 1 AND product_id = 1;

-- Изменение статуса заказа:
UPDATE orders
SET status = 'Отправлен'
WHERE id = 1;

-- Обновление статуса оплаты заказа:
UPDATE payments
SET payment_status = 'Оплачено'
WHERE order_id = 1;

-- Редактирование информации о поставщике:
UPDATE suppliers
SET contact_info = 'Телефон: +7 (123) 456-7899'
WHERE id = 1;


-- Обновление даты окончания скидки:
UPDATE discounts
SET end_date = '2024-11-30'  
WHERE id = 1;  


UPDATE users
SET is_superuser = TRUE
WHERE email = 'admin@gmail.com';



