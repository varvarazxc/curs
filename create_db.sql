-- ============================================================
-- БАЗА ДАННЫХ ДЛЯ ИНТЕРНЕТ-МАГАЗИНА МЕРЧА
-- ============================================================

-- 1. Создание базы данных
CREATE DATABASE IF NOT EXISTS merch_shop;
USE merch_shop;

-- 2. Таблица товаров
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    size VARCHAR(20),
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Таблица клиентов
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Таблица заказов
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('новый','оплачен','отправлен','доставлен','отменён') DEFAULT 'новый',
    total_amount DECIMAL(10,2),
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);

-- 5. Таблица состава заказа
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price_at_order DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- 6. Тестовые данные (товары)
INSERT INTO products (name, category, price, size, stock_quantity) VALUES
('Футболка "Рок-звезда"', 'Футболка', 1299.00, 'M', 25),
('Футболка "Рок-звезда"', 'Футболка', 1299.00, 'L', 20),
('Кружка с логотипом', 'Кружка', 599.00, NULL, 50),
('Постер "City Nights"', 'Постер', 899.00, 'A3', 15),
('Худи "Оверсайз"', 'Худи', 2499.00, 'XL', 10);

-- 7. Тестовые данные (клиенты)
INSERT INTO customers (full_name, email, phone, address) VALUES
('Иванов Пётр Сергеевич', 'ivanov@mail.ru', '+79111234567', 'г. Москва, ул. Тверская, д. 1'),
('Смирнова Анна Викторовна', 'anna.smirnova@yandex.ru', '+79219876543', 'г. Санкт-Петербург, Невский пр., д. 25'),
('Козлов Дмитрий Алексеевич', 'd.kozlov@gmail.com', '+79031234567', 'г. Екатеринбург, ул. Ленина, д. 10');

-- 8. Тестовые данные (заказы)
INSERT INTO orders (customer_id, status, total_amount, shipping_address) VALUES
(1, 'доставлен', 2597.00, 'г. Москва, ул. Тверская, д. 1'),
(1, 'отправлен', 1299.00, 'г. Москва, ул. Тверская, д. 1'),
(2, 'оплачен', 3497.00, 'г. Санкт-Петербург, Невский пр., д. 25'),
(3, 'новый', 1798.00, 'г. Екатеринбург, ул. Ленина, д. 10');

-- 9. Тестовые данные (состав заказов)
INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES
(1, 1, 1, 1299.00),
(1, 3, 2, 599.00),
(2, 1, 1, 1299.00),
(3, 2, 1, 1299.00),
(3, 5, 1, 2499.00),
(4, 4, 2, 899.00);