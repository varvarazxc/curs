import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'merch_shop'
}

def add_product(name, category, price, size, stock):
    """Добавление нового товара"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (name, category, price, size, stock_quantity) 
        VALUES (%s, %s, %s, %s, %s)
    """, (name, category, price, size, stock))
    conn.commit()
    conn.close()
    print("Товар успешно добавлен!")


def add_customer(full_name, email, phone, address):
    """Добавление нового клиента"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO customers (full_name, email, phone, address) 
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, phone, address))
        conn.commit()
        print("Клиент успешно добавлен!")
    except mysql.connector.IntegrityError:
        print("Ошибка: клиент с таким email уже существует!")
    conn.close()


def create_order(customer_id, items, shipping_address):

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        for product_id, quantity in items:
            cur.execute("SELECT stock_quantity FROM products WHERE id = %s", (product_id,))
            result = cur.fetchone()
            if not result:
                print(f"Товара с id {product_id} не существует!")
                return
            if result[0] < quantity:
                print(f"Товара с id {product_id} недостаточно на складе! Доступно: {result[0]}")
                return

        for product_id, quantity in items:
            cur.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s",
                        (quantity, product_id))

        cur.execute("""
            INSERT INTO orders (customer_id, shipping_address, status) 
            VALUES (%s, %s, 'новый')
        """, (customer_id, shipping_address))
        order_id = cur.lastrowid

        total = 0
        for product_id, quantity in items:
            cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cur.fetchone()[0]
            total += price * quantity
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price_at_order) 
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))

        cur.execute("UPDATE orders SET total_amount = %s WHERE id = %s", (total, order_id))
        conn.commit()
        print(f"Заказ №{order_id} оформлен на сумму {total:.2f} руб.")

    except Exception as e:
        print(f"Ошибка при оформлении заказа: {e}")
        conn.rollback()
    finally:
        conn.close()


def update_order_status(order_id, new_status):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    conn.commit()
    conn.close()
    print(f"Статус заказа №{order_id} изменён на '{new_status}'")


def get_popular_products():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.name AS товар,
            p.category AS категория,
            SUM(oi.quantity) AS всего_продано
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status IN ('оплачен', 'отправлен', 'доставлен')
        GROUP BY p.id
        ORDER BY всего_продано DESC
        LIMIT 5
    """)
    results = cur.fetchall()
    conn.close()
    return results


def get_revenue_by_category():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.category AS категория,
            SUM(oi.quantity * oi.price_at_order) AS выручка
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status IN ('оплачен', 'отправлен', 'доставлен')
        GROUP BY p.category
        ORDER BY выручка DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results


def get_active_customers():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.full_name AS клиент,
            c.email AS email,
            COUNT(o.id) AS количество_заказов,
            SUM(o.total_amount) AS сумма_покупок
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        WHERE o.status IN ('оплачен', 'отправлен', 'доставлен')
        GROUP BY c.id
        ORDER BY количество_заказов DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results


def get_stock():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            name AS товар,
            stock_quantity AS остаток
        FROM products
        ORDER BY stock_quantity DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results

def main_menu():
    while True:
        print("\n" + "=" * 40)
        print("        ИНТЕРНЕТ-МАГАЗИН МЕРЧА")
        print("=" * 40)
        print("1. Добавить товар")
        print("2. Добавить клиента")
        print("3. Оформить заказ")
        print("4. Изменить статус заказа")
        print("5. Отчёт: популярные товары")
        print("6. Отчёт: выручка по категориям")
        print("7. Отчёт: активные клиенты")
        print("8. Просмотр остатков товаров")
        print("0. Выход")
        print("=" * 40)

        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Название товара: ")
            category = input("Категория: ")
            price = float(input("Цена: "))
            size = input("Размер (если есть, нажмите Enter для пропуска): ")
            stock = int(input("Количество на складе: "))
            add_product(name, category, price, size, stock)

        elif choice == '2':
            full_name = input("ФИО клиента: ")
            email = input("Email: ")
            phone = input("Телефон: ")
            address = input("Адрес: ")
            add_customer(full_name, email, phone, address)

        elif choice == '3':
            try:
                customer_id = int(input("ID клиента: "))
                shipping_address = input("Адрес доставки: ")
                items = []
                print("\nВведите товары в заказ:")
                print("(для завершения введите ID товара 0)")
                while True:
                    product_id = int(input("ID товара (0 - завершить): "))
                    if product_id == 0:
                        break
                    quantity = int(input("Количество: "))
                    items.append((product_id, quantity))
                if items:
                    create_order(customer_id, items, shipping_address)
                else:
                    print("Заказ не может быть пустым!")
            except ValueError:
                print("Ошибка: введите корректное числовое значение!")

        elif choice == '4':
            try:
                order_id = int(input("ID заказа: "))
                print("\nДоступные статусы: новый, оплачен, отправлен, доставлен, отменён")
                new_status = input("Новый статус: ")
                valid_statuses = ['новый', 'оплачен', 'отправлен', 'доставлен', 'отменён']
                if new_status in valid_statuses:
                    update_order_status(order_id, new_status)
                else:
                    print("Ошибка: недопустимый статус!")
            except ValueError:
                print("Ошибка: введите корректное числовое значение!")

        elif choice == '5':
            results = get_popular_products()
            print("\n" + "=" * 50)
            print("САМЫЕ ПОПУЛЯРНЫЕ ТОВАРЫ")
            print("=" * 50)
            if results:
                print(f"{'Товар':<30} {'Категория':<15} {'Продано':<10}")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]:<30} {row[1]:<15} {row[2]:<10}")
            else:
                print("Нет данных о продажах.")

        elif choice == '6':
            results = get_revenue_by_category()
            print("\n" + "=" * 50)
            print("ВЫРУЧКА ПО КАТЕГОРИЯМ")
            print("=" * 50)
            if results:
                print(f"{'Категория':<20} {'Выручка':<15}")
                print("-" * 35)
                for row in results:
                    print(f"{row[0]:<20} {row[1]:<15.2f} руб.")
            else:
                print("Нет данных о продажах.")

        elif choice == '7':
            results = get_active_customers()
            print("\n" + "=" * 70)
            print("АКТИВНЫЕ КЛИЕНТЫ")
            print("=" * 70)
            if results:
                print(f"{'Клиент':<25} {'Email':<25} {'Заказов':<10} {'Сумма':<15}")
                print("-" * 70)
                for row in results:
                    print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10} {row[3]:<15.2f} руб.")
            else:
                print("Нет данных о клиентах.")

        elif choice == '8':
            results = get_stock()
            print("\n" + "=" * 40)
            print("ОСТАТКИ ТОВАРОВ НА СКЛАДЕ")
            print("=" * 40)
            if results:
                print(f"{'Товар':<30} {'Остаток':<10}")
                print("-" * 40)
                for row in results:
                    print(f"{row[0]:<30} {row[1]:<10}")
            else:
                print("Нет товаров на складе.")

        elif choice == '0':
            print("\nРабота завершена. До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите цифру от 0 до 8.")

if __name__ == "__main__":
    print("=" * 40)
    print("  ДОБРО ПОЖАЛОВАТЬ В ИНТЕРНЕТ-МАГАЗИН МЕРЧА!")
    print("=" * 40)
    main_menu()