Как запустить приложение

 1. Установить MySQL

Скачайте и установите MySQL с официального сайта.

 2. Создать базу данных

Выполните SQL-скрипт из файла `create_db.sql` в MySQL Workbench:

1. Откройте MySQL Workbench
2. Нажмите **File → Open SQL Script** и выберите файл `create_db.sql`
3. Нажмите кнопку с молнией ⚡ (Execute) или нажмите **Ctrl+Shift+Enter**
4. База данных `merch_shop` будет создана и заполнена тестовыми данными
   Запуск приложения на пайтоне

1. Установите Python 3
2. Установите библиотеку: `pip install mysql-connector-python`
3. Выполните `create_db.sql` в MySQL Workbench
4. В файле `dd.py` укажите свой пароль от MySQL
5. Запустите: `python dd.py`
