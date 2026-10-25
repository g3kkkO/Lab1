# Книжный магазин

Консольное приложение на Python для управления книжным магазином: авторы, книги,
издатели, жанры, клиенты и заказы. Поддерживает хранение данных в форматах JSON
и XML, автоматически сохраняет изменения после каждой операции.

## Возможности

- Авторы — добавление, просмотр, изменение имени, удаление.
- Книги — добавление, просмотр, изменение любого поля (название, авторы,
  издатель, год, жанры, цена, количество), удаление.
- Издатели — добавление, просмотр, изменение, удаление.
- Жанры — добавление, просмотр, изменение, удаление.
- Клиенты — добавление (имя, email), просмотр, изменение имени/email, удаление.
- Заказы — создание с позициями (product_id:quantity), просмотр,
  изменение статуса/адреса/позиций/суммы, удаление.
- Валидация: имя, email, цена, год,
  статус заказа (new/paid/shipped/delivered/cancelled), ID.
- Выбор формата: `--fmt json` или `--fmt xml` (по умолчанию `json`).
- Обработка ошибок: собственные исключения для валидации.

## Структура проекта

    .
    ├── core/
    │   ├── exceptions.py        # собственные исключения
    │   ├── manager.py           # менеджер репозиториев
    │   └── validation_helper.py # валидация имён, email, цены, адреса
    ├── models/                  # модели предметной области
    │   ├── authors.py
    │   ├── books.py
    │   ├── customers.py
    │   ├── genres.py
    │   ├── orders.py
    │   ├── order_items.py
    │   └── publishers.py
    ├── repositories/            # доступ к файлам (CRUD операции)
    │   ├── authors_repo.py
    │   ├── books_repo.py
    │   ├── customer_repo.py
    │   ├── genres_repo.py
    │   ├── orders_repo.py
    │   └── publisher_repo.py
    ├── services/                # бизнес-логика и валидация
    │   ├── author_service.py
    │   ├── book_service.py
    │   ├── customer_service.py
    │   ├── genres_service.py
    │   ├── orders_service.py
    │   └── publisher_service.py
    ├── data/
    │   ├── authors.json
    │   ├── books.json
    │   ├── customers.json
    │   ├── genres.json
    │   ├── orders.json
    │   ├── publishers.json
    │   ├── authors.xml
    │   ├── books.xml
    │   ├── customers.xml
    │   ├── genres.xml
    │   ├── orders.xml
    │   └── publishers.xml
    ├── main.py                  # CLI (argparse), точка входа
    ├── pyproject.toml
    ├── uv.lock
    └── README.md

## Модули

| Файл | Что содержит |
|------|--------------|
| core/exceptions.py | FormatFileError, IdTypeError, NameTypeError, YearValueError, PriceValueError, StockValueError, StatusValueError, InvalidEmailError, AuthorNotFound, BookNotFound, CustomerNotFound, GenreNotFound, OrderNotFound, PublisherNotFound |
| core/manager.py | Manager — создаёт репозитории на data/<entity>.<fmt> |
| core/validation_helper.py | validate_name, validate_email, validate_address, validate_price |
| models/*.py | модели с to_dict / from_dict |
| repositories/*.py | CRUD для JSON и XML |
| services/*.py | валидация + вызовы репозитория |
| main.py | argparse CLI: --list, --create-*, --update-*, --delete |

## Установка и запуск

    git clone https://github.com/g3kkkO/Lab1.git
    cd Lab1
Способ 1: с использованием uv

    uv run main.py --help
Способ 2: классическое виртуальное окружение

**Windows:**

    python -m venv venv
    venv\Scripts\activate
    python main.py --help
    
**macOS / Linux:**

    python3 -m venv venv
    source venv/bin/activate
    python3 main.py --help
  

**Далее замените uv run на python.**

## Как пользоваться

CLI построен на argparse. Формат задаётся флагом `--fmt` (json / xml).

Список всех записей сущности:

    uv run main.py --list author
    uv run main.py --list book
    uv run main.py --list customer
    uv run main.py --list genre
    uv run main.py --list order
    uv run main.py --list publisher

Создание:

    uv run main.py --create-author "Лев Толстой"
    uv run main.py --create-genre "Роман"
    uv run main.py --create-publisher "Эксмо"
    uv run main.py --create-customer "Иван Петров" "ivan@example.com"
    uv run main.py --create-book "Война и мир" 1 1 1869 1,4 1200 10
    uv run main.py --create-order 1 new "Площадь" "1:2,3:1"

Изменение:

    uv run main.py --update-name author 1 "Лев Николаевич Толстой"
    uv run main.py --update-email 1 "new@example.com"
    uv run main.py --update-book-title 1 "Война и мир (т. 1)"
    uv run main.py --update-book-authors 1 "1,2"
    uv run main.py --update-book-publisher 1 2
    uv run main.py --update-book-year 1 1870
    uv run main.py --update-book-genres 1 "1,2,4"
    uv run main.py --update-book-price 1 999
    uv run main.py --update-book-stock 1 5
    uv run main.py --update-order-status 1 paid
    uv run main.py --update-order-address 1 "пр. Мира, 5"

Удаление:

    uv run main.py --delete author 1
    uv run main.py --delete book 1
    uv run main.py --delete order 1

С XML:

    uv run main.py --fmt xml --list author
    uv run main.py --fmt xml --create-author "Лев Толстой"

## Пример работы

    $ uv run main.py --create-author "Лев Толстой"
    Author успешно создан:
    {
        "author_id": 1,
        "name": "Лев Толстой"
    }

    $ uv run main.py --list author
    [
        {
            "author_id": 1,
            "name": "Лев Толстой"
        }
    ]

## Формат данных

JSON (data/authors.json):

    [
      {
        "author_id": 1,
        "name": "Лев Толстой"
      }
    ]

JSON (data/books.json):

    [
      {
        "book_id": 1,
        "title": "Война и мир",
        "author_ids": [1],
        "publisher_id": 1,
        "year": 1869,
        "genres_ids": [1, 4],
        "price": 1200.0,
        "stock": 10
      }
    ]

JSON (data/orders.json):

    [
      {
        "order_id": 1,
        "customer_id": 1,
        "items": [
          {
            "product_id": 1,
            "name": "Война и мир",
            "price_at_purchase": 1200.0,
            "quantity": 2
          }
        ],
        "status": "new",
        "created_at": "2026-10-25T12:00:00",
        "address": "Площадь",
        "total": 2400.0
      }
    ]

XML (data/books.xml):

    <?xml version="1.0" encoding="utf-8"?>
    <books>
      <book>
        <book_id>1</book_id>
        <title>Война и мир</title>
        <author_ids>
          <id>1</id>
        </author_ids>
        <publisher_id>1</publisher_id>
        <year>1869</year>
        <genres_ids>
          <id>1</id>
          <id>4</id>
        </genres_ids>
        <price>1200.0</price>
        <stock>10</stock>
      </book>
    </books>

XML (data/orders.xml):

    <?xml version="1.0" encoding="utf-8"?>
    <orders>
      <order>
        <order_id>1</order_id>
        <customer_id>1</customer_id>
        <items>
          <item>
            <product_id>1</product_id>
            <name>Война и мир</name>
            <price_at_purchase>1200.0</price_at_purchase>
            <quantity>2</quantity>
          </item>
        </items>
        <status>new</status>
        <created_at>2026-10-25T12:00:00</created_at>
        <address>Площадь</address>
        <total>2400.0</total>
      </order>
    </orders>

## Обработка ошибок

Все доменные ошибки — наследники Exception и ловятся в main.py
общим `except Exception` с выводом `Ошибка: <message>`:

| Исключение | Когда возникает |
|------------|-----------------|
| IdTypeError | ID не число / <= 0 |
| NameTypeError | имя не прошло validate_name |
| YearValueError | год не число / вне 1..current_year |
| PriceValueError | цена не число / <= 0 |
| StockValueError | склад не число |
| StatusValueError | статус не из VALID_STATUSES |
| InvalidEmailError | email не прошёл validate_email |
| AuthorNotFound / BookNotFound / … | сущность с таким ID не найдена |
| FormatFileError | расширение файла не json / xml |

## Особенности реализации

- ООП-модель: Author, Book, Customer, Genre, Publisher, OrderItems, Order —
  каждая с to_dict / from_dict.
- Аннотации типов у всех публичных методов.
- Разделение слоёв: models → repositories → services → main.
- Никаких сторонних зависимостей — только стандартная библиотека
- uv — управление окружением и запуском 
- Соблюдение PEP 8.
