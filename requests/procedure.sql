CREATE OR REPLACE PROCEDURE add_product_to_cart(user_id_param INT, 
												product_id_param INT, 
   												quantity_param INT)
LANGUAGE plpgsql AS $$
BEGIN
    -- Проверяем, есть ли у пользователя корзина
    PERFORM 1 FROM carts WHERE user_id = user_id_param;

    IF NOT FOUND THEN
        INSERT INTO carts (user_id) VALUES (user_id_param);
    END IF;

    -- Добавляем товар в корзину или обновляем количество, если товар уже есть
    INSERT INTO cart_products (cart_id, product_id, quantity)
    VALUES (
        (SELECT id FROM carts WHERE user_id = user_id_param),
        product_id_param,
        quantity_param
    )
    ON CONFLICT (cart_id, product_id) DO UPDATE
        SET quantity = cart_products.quantity + EXCLUDED.quantity;
END;
$$;


CREATE OR REPLACE PROCEDURE add_product_to_order(order_id INT, product_id INT, quantity INT)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO order_products (order_id, product_id, quantity)
    VALUES (order_id, product_id, quantity);

END;
$$;

CREATE OR REPLACE PROCEDURE update_order_status(order_id INT, new_status VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE orders
    SET status = new_status
    WHERE id = order_id;
END;
$$;


CREATE OR REPLACE PROCEDURE add_discount(product_id INT, discount_amount DECIMAL, start_date DATE, end_date DATE)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO discounts (product_id, discount_amount, start_date, end_date)
    VALUES (product_id, discount_amount, start_date, end_date);
END;
$$;
