CREATE OR REPLACE FUNCTION log_update_order_total()
RETURNS TRIGGER AS $$
BEGIN
    
    UPDATE orders
    SET total_amount = (
        SELECT SUM(op.quantity * p.price)
        FROM order_products op
        JOIN products p ON op.product_id = p.id
        WHERE op.order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для обновления суммы заказа
CREATE OR REPLACE TRIGGER trigger_update_order_total
AFTER INSERT OR UPDATE ON order_products
FOR EACH ROW
EXECUTE FUNCTION log_update_order_total();


----------------------------------------------------------------------------------------




CREATE OR REPLACE FUNCTION log_update_product_stock()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновляем количество товара на складе
    UPDATE products
    SET stock = stock - NEW.quantity
    WHERE id = NEW.product_id;

    -- Логируем действие
    INSERT INTO audit_logs (user_id, action, timestamp)
    VALUES (
        COALESCE(NEW.user_id, 0),  
        'Обновление склада: Товар ID ' || NEW.product_id || ', уменьшение на ' || NEW.quantity,
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для обновления склада
CREATE TRIGGER trigger_update_product_stock
AFTER INSERT ON order_products
FOR EACH ROW
EXECUTE FUNCTION log_update_product_stock();


-------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION log_user_action()
RETURNS TRIGGER AS $$
DECLARE
    extracted_user_id INT;
BEGIN
    -- Извлекаем user_id в зависимости от таблицы
    IF TG_TABLE_NAME = 'users' THEN
        extracted_user_id := NEW.id;
    ELSIF TG_TABLE_NAME = 'cart_products' THEN
        SELECT user_id INTO extracted_user_id
        FROM carts
        WHERE id = COALESCE(NEW.cart_id, OLD.cart_id);
    ELSE
        extracted_user_id := COALESCE(NEW.user_id, OLD.user_id);
    END IF;

    -- Вставляем запись в таблицу audit_logs
    INSERT INTO audit_logs (user_id, action, timestamp)
    VALUES (
        COALESCE(extracted_user_id, 0),  
        TG_OP || ' на таблицу ' || TG_TABLE_NAME || ': данные ' ||
        CASE
            WHEN TG_OP = 'INSERT' THEN row_to_json(NEW)::TEXT
            WHEN TG_OP = 'UPDATE' THEN 'Старые данные: ' || row_to_json(OLD)::TEXT || ', Новые данные: ' || row_to_json(NEW)::TEXT
            WHEN TG_OP = 'DELETE' THEN row_to_json(OLD)::TEXT
        END,
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_review_insert
AFTER INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION log_user_action();

CREATE TRIGGER trigger_log_order_insert
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION log_user_action();

CREATE TRIGGER trigger_log_cart_update
AFTER INSERT OR UPDATE OR DELETE ON cart_products
FOR EACH ROW
EXECUTE FUNCTION log_user_action();

CREATE TRIGGER trigger_log_user_insert
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_action();

----------------------------------------------------------------------


CREATE OR REPLACE FUNCTION remove_expired_discounts()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM discounts WHERE end_date < CURRENT_DATE;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_remove_expired_discounts
AFTER INSERT OR UPDATE ON discounts
FOR EACH ROW
EXECUTE FUNCTION remove_expired_discounts();


