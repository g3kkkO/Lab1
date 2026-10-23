import os

from core.manager import Manager
from core.exceptions import (
    IdTypeError, NameTypeError, YearValueError, PriceValueError,
    StockValueError, StatusValueError, InvalidEmailError,
    AuthorNotFound, BookNotFound, CustomerNotFound, GenreNotFound,
    OrderNotFound, PublisherNotFound,
)
from services.author_service import AuthorService
from services.book_service import BookService
from services.customer_service import CustomerService
from services.genres_service import GenreService
from services.orders_service import OrderService
from services.publisher_service import PublisherService


# Очистка экрана (кроссплатформенно)
def clear() -> None:
    os.system("clear" if os.name != "nt" else "cls")


# Пауза до нажатия Enter
def pause() -> None:
    input("\nEnter — продолжить...")


# Вывод ошибки в читаемом виде
def show_error(e: Exception) -> None:
    print(f"\n[Ошибка] {type(e).__name__}: {e}")


# Главное меню: выбор сущности
def ask_entity() -> str | None:
    clear()
    print("=== ГЛАВНОЕ МЕНЮ ===")
    print("1. Авторы")
    print("2. Книги")
    print("3. Клиенты")
    print("4. Жанры")
    print("5. Заказы")
    print("6. Издатели")
    print("0. Выход")
    choice = input("\nВыбор: ").strip()

    return {
        "1": "author", "2": "book", "3": "customer",
        "4": "genre", "5": "order", "6": "publisher",
        "0": None,
    }.get(choice)


# Меню выбора формата файла (JSON/XML)
def ask_format() -> str | None:
    clear()
    print("=== ФОРМАТ ФАЙЛА ===")
    print("1. JSON")
    print("2. XML")
    print("0. Назад")
    choice = input("\nВыбор: ").strip()

    return {"1": "json", "2": "xml", "0": None}.get(choice)


# Фабрика сервисов: сущность → сервис
def make_service(entity: str, db: Manager):
    return {
        "author":    AuthorService,
        "book":      BookService,
        "customer":  CustomerService,
        "genre":     GenreService,
        "order":     OrderService,
        "publisher": PublisherService,
    }[entity](db)


# Меню действий (CRUD) для выбранной сущности
def actions_menu(service, entity_name: str) -> None:
    while True:
        clear()
        print(f"=== {entity_name.upper()} ===")
        print("1. Список")
        print("2. Создать")
        print("3. Изменить")
        print("4. Удалить")
        print("0. Назад")
        choice = input("\nВыбор: ").strip()

        try:
            # READ: список всех записей
            if choice == "1":
                items = service.get_all() if hasattr(service, "get_all") else []
                clear()
                if not items:
                    print("(пусто)")
                for obj in items:
                    print(obj.to_dict())
                pause()

            # CREATE: создание записи
            elif choice == "2":
                create_flow(service, entity_name)
                pause()

            # UPDATE: изменение записи
            elif choice == "3":
                update_flow(service, entity_name)
                pause()

            # DELETE: удаление записи
            elif choice == "4":
                delete_flow(service, entity_name)
                pause()

            # Назад в главное меню
            elif choice == "0":
                return

            else:
                print("Нет такой команды.")
                pause()

        # Ловим доменные исключения и печатаем понятное сообщение
        except (IdTypeError, NameTypeError, YearValueError, PriceValueError,
                StockValueError, StatusValueError, InvalidEmailError,
                AuthorNotFound, BookNotFound, CustomerNotFound, GenreNotFound,
                OrderNotFound, PublisherNotFound) as e:
            show_error(e)
            pause()
        # Ловим прочие исключения (чтобы меню не падало)
        except Exception as e:
            show_error(e)
            pause()


def parse_order_items(raw: str) -> list[dict]:
    text = raw.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    items = []
    for part in text.split(","):
        clean = part.strip().strip("()[]{}")
        if not clean:
            continue
        if ":" not in clean:
            raise ValueError("Позиции должны быть в формате product_id:quantity")
        pid, qty = clean.split(":", 1)
        items.append({
            "product_id": pid.strip().strip("()[]{}"),
            "quantity": qty.strip().strip("()[]{}"),
        })

    if not items:
        raise ValueError("Не указаны позиции заказа")
    return items


# CREATE: ввод полей и создание записи
def create_flow(service, entity_name: str) -> None:
    clear()
    print(f"--- Создание ({entity_name}) ---")
    if entity_name == "author":
        name = input("Имя: ")
        obj = service.create_author(name)
    elif entity_name == "genre":
        name = input("Название жанра: ")
        obj = service.create_genre(name)
    elif entity_name == "publisher":
        name = input("Название издателя: ")
        obj = service.create_publisher(name)
    elif entity_name == "customer":
        name = input("Имя: ")
        email = input("Email: ")
        obj = service.create_customer(name, email)
    elif entity_name == "book":
        title = input("Название книги: ")
        author_ids = input("ID авторов (через запятую): ").split(",")
        publisher_id = input("ID издателя: ")
        year = input("Год: ")
        genres_ids = input("ID жанров (через запятую): ").split(",")
        price = input("Цена: ")
        stock = input("Склад: ")
        obj = service.create_book(title, author_ids, publisher_id,
                                  year, genres_ids, price, stock)
    elif entity_name == "order":
        customer_id = input("ID клиента: ")
        status = input("Статус (new/paid/shipped/delivered/cancelled): ")
        address = input("Адрес: ")
        raw = input("Позиции (product_id:quantity,...): ")
        items = parse_order_items(raw)
        obj = service.create_order(customer_id, items, status, address)
    else:
        print("Нет такого действия.")
        return

    print(f"\nСоздано: {obj.to_dict()}")


# UPDATE: выбор поля и изменение записи
def update_flow(service, entity_name: str) -> None:
    clear()
    print(f"--- Изменение ({entity_name}) ---")

    if entity_name == "author":
        author_id = input("ID автора: ").strip()
        new_name = input("Новое имя: ").strip()
        obj = service.update_name(author_id, new_name)
        print(f"\nОбновлено: {obj.to_dict()}")

    elif entity_name == "genre":
        genre_id = input("ID жанра: ").strip()
        new_name = input("Новое название: ").strip()
        obj = service.update_name(genre_id, new_name)
        print(f"\nОбновлено: {obj.to_dict()}")

    elif entity_name == "publisher":
        publisher_id = input("ID издателя: ").strip()
        new_name = input("Новое название: ").strip()
        obj = service.update_name(publisher_id, new_name)
        print(f"\nОбновлено: {obj.to_dict()}")

    elif entity_name == "customer":
        print("1. Имя")
        print("2. Email")
        field = input("Что менять: ").strip()
        customer_id = input("ID клиента: ").strip()
        if field == "1":
            obj = service.update_name(customer_id, input("Новое имя: ").strip())
        elif field == "2":
            obj = service.update_email(customer_id, input("Новый email: ").strip())
        else:
            print("Нет такого поля.")
            return
        print(f"\nОбновлено: {obj.to_dict()}")

    elif entity_name == "book":
        print("1. Название")
        print("2. Авторы")
        print("3. Издатель")
        print("4. Год")
        print("5. Жанры")
        print("6. Цена")
        print("7. Склад")
        field = input("Что менять: ").strip()
        book_id = input("ID книги: ").strip()

        if field == "1":
            obj = service.update_title(book_id, input("Новое название: ").strip())
        elif field == "2":
            ids = input("ID авторов (через запятую): ").split(",")
            obj = service.update_author_ids(book_id, ids)
        elif field == "3":
            obj = service.update_publisher_id(book_id, input("ID издателя: ").strip())
        elif field == "4":
            obj = service.update_year(book_id, input("Год: ").strip())
        elif field == "5":
            ids = input("ID жанров (через запятую): ").split(",")
            obj = service.update_genres(book_id, ids)
        elif field == "6":
            obj = service.update_price(book_id, input("Цена: ").strip())
        elif field == "7":
            obj = service.update_stock(book_id, input("Склад: ").strip())
        else:
            print("Нет такого поля.")
            return
        print(f"\nОбновлено: {obj.to_dict()}")

    elif entity_name == "order":
        print("1. Статус")
        print("2. Адрес")
        print("3. Позиции")
        print("4. Сумма")
        field = input("Что менять: ").strip()
        order_id = input("ID заказа: ").strip()

        if field == "1":
            obj = service.update_status(order_id, input("Новый статус: ").strip())
        elif field == "2":
            obj = service.update_address(order_id, input("Новый адрес: ").strip())
        elif field == "3":
            raw = input("Позиции (product_id:quantity,...): ").strip()
            items = parse_order_items(raw)
            obj = service.update_items(order_id, items)
        elif field == "4":
            obj = service.update_total(order_id, input("Новая сумма: ").strip())
        else:
            print("Нет такого поля.")
            return
        print(f"\nОбновлено: {obj.to_dict()}")

    else:
        print("Нет такого действия.")


# DELETE: удаление записи по ID
def delete_flow(service, entity_name: str) -> None:
    clear()
    print(f"--- Удаление ({entity_name}) ---")
    raw_id = input("ID: ")
    if entity_name == "author":
        service.delete_author(raw_id)
    elif entity_name == "book":
        service.delete_book(raw_id)
    elif entity_name == "customer":
        service.delete_customer(raw_id)
    elif entity_name == "genre":
        service.delete_genre(raw_id)
    elif entity_name == "order":
        service.delete_order(raw_id)
    elif entity_name == "publisher":
        service.delete_publisher(raw_id)
    else:
        print("Нет такого действия.")
        return
    print("Удалено.")


# Точка входа: главное меню → формат → действия
def main() -> None:
    while True:
        entity = ask_entity()
        if entity is None:
            clear()
            print("Выход.")
            return

        fmt = ask_format()
        if fmt is None:
            continue                      # назад в главное меню

        db = Manager("data", fmt)         # путь выбран один раз
        service = make_service(entity, db)
        actions_menu(service, entity)     # 0 → назад к выбору сущности


if __name__ == "__main__":
    main()