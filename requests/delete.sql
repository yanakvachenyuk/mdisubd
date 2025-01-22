-- Удаление товара по его идентификатору

DELETE FROM products
WHERE id = 6;  


-- Удаление всех товаров определённой категории

DELETE FROM products
WHERE category_id = 2;  


-- Удаление поставщика и связанных с ним товаров (с использованием CASCADE)

DELETE FROM Suppliers
WHERE Id = 4;  -- Удаление поставщика с идентификатором 4 и всех связанных товаров


DELETE FROM users WHERE id = 1;