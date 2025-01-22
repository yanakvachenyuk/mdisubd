-- Добавление колонки supplier_id в таблицу products
ALTER TABLE products
ADD COLUMN supplier_id INT;

-- Установка внешнего ключа для таблицы suppliers
ALTER TABLE products
ADD CONSTRAINT fk_supplier
FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE;

