# Описание сущностей

## 1. User (Пользователь):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор.
name (VARCHAR) — имя пользователя.
email (VARCHAR, UNIQUE) — уникальный email.
password (VARCHAR) — пароль.
address (TEXT) — адрес доставки.
role_id (FK, INT) — связь с таблицей Role.
profile_id (FK, INT) — ссылка на профиль пользователя (связь один к одному с таблицей Profile).

**Связи:**
Один ко многим с таблицей Order.
Один ко многим с таблицей Review.
Один к одному с таблицей Profile (каждый пользователь имеет уникальный профиль).

## 2. Profile (Профиль):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор профиля.
phone_number (VARCHAR) — номер телефона.
birth_date (DATE) — дата рождения.
gender (VARCHAR) — пол.

**Связи:**
Один к одному с таблицей User.

## 3. Product (Товар):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор товара.
name (VARCHAR) — название товара.
description (TEXT) — описание товара.
price (DECIMAL) — цена товара.
category_id (FK, INT) — ссылка на категорию товара.
stock (INT) — количество товара в наличии.

**Связи:**
Один ко многим с таблицей Category.
Многие ко многим с таблицей Order через OrderItem.
Один ко многим с таблицей Review.

## 4. Category (Категория):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор.
name (VARCHAR) — название категории.

**Связи:**
Один ко многим с таблицей Product.

## 5. Order (Заказ):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор заказа.
user_id (FK, INT) — ссылка на пользователя.
order_date (DATE) — дата заказа.
status (VARCHAR) — статус заказа (например, «в обработке», «отправлен»).

**Связи:**
Один ко многим с таблицей User.
Многие ко многим с таблицей Product через OrderItem.

## 6. OrderItem (Элемент заказа):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор.
order_id (FK, INT) — ссылка на заказ.
product_id (FK, INT) — ссылка на товар.
quantity (INT) — количество товаров.

**Связи:**
Многие ко многим между таблицами Order и Product.

## 7. Review (Отзыв):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор отзыва.
user_id (FK, INT) — ссылка на пользователя.
product_id (FK, INT) — ссылка на товар.
rating (INT) — оценка (например, от 1 до 5).
comment (TEXT) — комментарий.

**Связи:**
Один ко многим с таблицей User.
Один ко многим с таблицей Product.

## 8. Cart (Корзина):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор корзины.
user_id (FK, INT) — ссылка на пользователя.

**Связи:**
Один к одному с таблицей User.
Многие ко многим с таблицей Product.

## 9. CartItem:

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор.
cart_id (FK, INT) — ссылка на корзину.
product_id (FK, INT) — ссылка на товар.
quantity (INT) — количество товаров.

**Связи:**
Многие ко многим между таблицами Order и Product.

## 10. Payment (Оплата):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор оплаты.
order_id (FK, INT) — ссылка на заказ.
payment_status (VARCHAR) — статус оплаты.

**Связи:**
Один к одному с таблицей Order (каждый заказ связан с одной оплатой).

## 11. AuditLog (Журнал действий):

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор записи.
user_id (FK, INT) — ссылка на пользователя.
action (TEXT) — описание действия.
timestamp (DATETIME) — время выполнения действия.

**Связи:**
Один ко многим с таблицей User.

## 12. Supplier (Поставщик)

**Поля:**
id (PK, INT, AUTO_INCREMENT) — уникальный идентификатор.
name (VARCHAR) — имя поставщика.
contact_info (TEXT) — контактная информация.

**Связи:**
Один ко многим с таблицей Product (каждый товар связан с поставщиком).
