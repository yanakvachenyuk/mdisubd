INSERT INTO users (name, email, password, address, is_superuser) VALUES
('Иван Иванов', 'ivanov@example.com', 'password123', 'Москва, ул. Ленина, д. 1', FALSE),
('Мария Петрова', 'petrova@example.com', 'password123', 'Санкт-Петербург, пр. Невский, д. 2', TRUE),
('Сергей Сидоров', 'sidorov@example.com', 'password123', 'Екатеринбург, ул. Челюскинцев, д. 3', FALSE);


INSERT INTO categories (name) VALUES
('Одежда'),
('Обувь'),
('Аксессуары'),
('Спортивная одежда');


INSERT INTO products (name, description, price, category_id, stock, supplier_id) VALUES
('Футболка', 'Стильная футболка из хлопка', 19.99, 1, 100, 1),
('Джинсы', 'Удобные джинсы с высокой талией', 49.99, 1, 50, 2),
('Кроссовки', 'Легкие кроссовки для бега', 69.99, 2, 75, 1),
('Сумка', 'Элегантная сумка на каждый день', 29.99, 3, 30, 3),
('Спортивный костюм', 'Костюм для тренировок', 59.99, 4, 40, 1);


INSERT INTO orders (user_id, order_date, status) VALUES
(1, '2024-10-01', 'Завершен'),
(2, '2024-10-05', 'В процессе'),
(3, '2024-10-10', 'Отменен');



INSERT INTO order_products (order_id, product_id, quantity) VALUES
(1, 6, 2),  
(1, 7, 1),  
(2, 8, 1),  
(3, 6, 1),  
(3, 9, 1);  


INSERT INTO reviews (user_id, product_id, rating, comment) VALUES
(1, 6, 5, 'Отличная футболка, очень комфортная!'),
(2, 7, 4, 'Джинсы сидят хорошо, но могли бы быть чуть длиннее.'),
(1, 8, 5, 'Лучшие кроссовки, которые я когда-либо носил!'),
(3, 9, 3, 'Сумка хорошая, но ожидал большего.');


INSERT INTO carts (user_id) VALUES
(1),
(2),
(3);


INSERT INTO cart_products (cart_id, product_id, quantity) VALUES
(1, 6, 1),  
(1, 7, 1),  
(2, 8, 2),  
(3, 9, 1);  


INSERT INTO payments (order_id, payment_status) VALUES
(1, 'Оплачено'),
(2, 'Ожидание оплаты'),
(3, 'Возврат');


INSERT INTO audit_logs (user_id, action) VALUES
(1, 'Создал заказ #1'),
(2, 'Создал заказ #2'),
(3, 'Отменил заказ #3');


INSERT INTO suppliers (name, contact_info) VALUES
('Поставщик 1', 'Телефон: +7 (123) 456-7890'),
('Поставщик 2', 'Телефон: +7 (234) 567-8901'),
('Поставщик 3', 'Телефон: +7 (345) 678-9012');


INSERT INTO discounts (product_id, discount_amount, start_date, end_date) VALUES
(6, 5.00, '2024-10-01', '2024-10-31'),  
(7, 10.00, '2024-10-05', '2024-10-20');  
