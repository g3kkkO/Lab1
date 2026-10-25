import json
import argparse
from core.manager import Manager
from services.author_service import AuthorService
from services.book_service import BookService
from services.customer_service import CustomerService
from services.genres_service import GenreService
from services.orders_service import OrderService
from services.publisher_service import PublisherService


def get_service(entity: str, fmt: str):
    """Фабрика для инициализации нужного сервиса и менеджера БД."""
    db = Manager("data", fmt)
    services = {
        "author": AuthorService,
        "book": BookService,
        "customer": CustomerService,
        "genre": GenreService,
        "order": OrderService,
        "publisher": PublisherService,
    }
    if entity not in services:
        raise ValueError(f"Неизвестная сущность: {entity}")
    return services[entity](db)



def list_items(entity: str, fmt: str):
    """Выводит список всех записей выбранной сущности."""
    try:
        service = get_service(entity, fmt)
        items = service.get_all() if hasattr(service, "get_all") else []
        
        if items:
            results = [obj.to_dict() for obj in items]
            print(json.dumps(results, indent=4, ensure_ascii=False))
        else:
            print(f"Записи для '{entity}' не найдены.")
    except Exception as e:
        print(f"Ошибка: {e}")



def create_named_entity(entity: str, name: str, fmt: str):
    """Универсальное создание сущностей с одним полем (Автор, Жанр, Издатель)."""
    try:
        service = get_service(entity, fmt)
        if entity == "author": obj = service.create_author(name)
        elif entity == "genre": obj = service.create_genre(name)
        elif entity == "publisher": obj = service.create_publisher(name)
        
        print(f"{entity.capitalize()} успешно создан:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def create_customer(name: str, email: str, fmt: str):
    """Создает нового клиента."""
    try:
        service = get_service("customer", fmt)
        obj = service.create_customer(name, email)
        print("Клиент успешно создан:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def create_book(title: str, authors: str, pub_id: str, year: str, genres: str, price: str, stock: str, fmt: str):
    """Создает новую книгу."""
    try:
        service = get_service("book", fmt)
        obj = service.create_book(
            title, authors.split(","), pub_id, year, genres.split(","), price, stock
        )
        print("Книга успешно создана:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def create_order(customer_id: str, status: str, address: str, raw_items: str, fmt: str):
    """Создает новый заказ (формат items: '1:2,3:1' -> id:кол-во)."""
    try:
        service = get_service("order", fmt)
        items = []
        for pair in raw_items.split(","):
            pid, qty = pair.split(":")
            items.append({"product_id": pid.strip(), "quantity": qty.strip()})
            
        obj = service.create_order(customer_id, items, status, address)
        print("Заказ успешно создан:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")



def update_name(entity: str, item_id: str, new_name: str, fmt: str):
    """Обновляет имя/название для автора, жанра, издателя или клиента."""
    try:
        service = get_service(entity, fmt)
        obj = service.update_name(item_id, new_name)
        print("Имя/название успешно обновлено:")
        if hasattr(obj, "to_dict"):
            print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def update_email(customer_id: str, new_email: str, fmt: str):
    """Обновляет email клиента."""
    try:
        service = get_service("customer", fmt)
        obj = service.update_email(customer_id, new_email)
        print("Email клиента успешно обновлен:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def update_book_field(book_id: str, field_name: str, value: str, fmt: str):
    """Универсальный обработчик для обновления конкретного поля книги."""
    try:
        service = get_service("book", fmt)
        
        if field_name == "title":
            obj = service.update_title(book_id, value)
        elif field_name == "authors":
            obj = service.update_author_ids(book_id, value.split(","))
        elif field_name == "publisher":
            obj = service.update_publisher_id(book_id, value)
        elif field_name == "year":
            obj = service.update_year(book_id, value)
        elif field_name == "genres":
            obj = service.update_genres(book_id, value.split(","))
        elif field_name == "price":
            obj = service.update_price(book_id, value)
        elif field_name == "stock":
            obj = service.update_stock(book_id, value)
            
        print(f"Поле '{field_name}' книги {book_id} успешно обновлено:")
        print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")

def update_order_field(order_id: str, field_name: str, value: str, fmt: str):
    """Обработчик обновления полей заказа."""
    try:
        service = get_service("order", fmt)
        if field_name == "status":
            service.update_status(order_id, value)
            print(f"Статус заказа {order_id} изменен на '{value}'.")
        elif field_name == "address":
            obj = service.update_address(order_id, value)
            print("Адрес доставки успешно обновлен:")
            print(json.dumps(obj.to_dict(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Ошибка: {e}")


def delete_item(entity: str, item_id: str, fmt: str):
    """Удаляет запись по ID."""
    try:
        service = get_service(entity, fmt)
        
        if entity == "author":
            service.delete_author(item_id)
        elif entity == "book":
            service.delete_book(item_id)
        elif entity == "customer":
            service.delete_customer(item_id)
        elif entity == "genre":
            service.delete_genre(item_id)
        elif entity == "order":
            service.delete_order(item_id)
        elif entity == "publisher":
            service.delete_publisher(item_id)
            
        print(f"Запись '{entity}' с ID {item_id} успешно удалена.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Утилита для работы с книжным магазином (CRUD)")
    
    parser.add_argument('--fmt', type=str, choices=['json', 'xml'], default='json', 
                        help="Формат хранения данных (по умолчанию: json)")
    
    parser.add_argument('--list', type=str, metavar='ENTITY', 
                        help="Вывести список записей (author, book, customer, genre, order, publisher)")
    
    parser.add_argument('--create-author', type=str, metavar='NAME', help="Создать автора")
    parser.add_argument('--create-genre', type=str, metavar='NAME', help="Создать жанр")
    parser.add_argument('--create-publisher', type=str, metavar='NAME', help="Создать издателя")
    parser.add_argument('--create-customer', nargs=2, type=str, metavar=('NAME', 'EMAIL'), help="Создать клиента")
    parser.add_argument('--create-book', nargs=7, type=str, metavar=('TITLE', 'AUTHORS', 'PUB_ID', 'YEAR', 'GENRES', 'PRICE', 'STOCK'),help="Создать книгу (ID списком через запятую)")
    parser.add_argument('--create-order', nargs=4, type=str, metavar=('CUST_ID', 'STATUS', 'ADDRESS', 'ITEMS'), help="Создать заказ (ITEMS в формате id:qty,id:qty)")
    
    parser.add_argument('--update-name', nargs=3, type=str, metavar=('ENTITY', 'ID', 'NEW_NAME'),help="Обновить имя/название (author, genre, publisher, customer)")
    parser.add_argument('--update-email', nargs=2, type=str, metavar=('CUST_ID', 'NEW_EMAIL'), help="Обновить email клиента")
    parser.add_argument('--update-book-title', nargs=2, metavar=('ID', 'TITLE'), help="Обновить название книги")
    parser.add_argument('--update-book-authors', nargs=2, metavar=('ID', 'AUTHORS'), help="Обновить авторов (ID через запятую)")
    parser.add_argument('--update-book-publisher', nargs=2, metavar=('ID', 'PUB_ID'), help="Обновить ID издателя")
    parser.add_argument('--update-book-year', nargs=2, metavar=('ID', 'YEAR'), help="Обновить год издания")
    parser.add_argument('--update-book-genres', nargs=2, metavar=('ID', 'GENRES'), help="Обновить жанры (ID через запятую)")
    parser.add_argument('--update-book-price', nargs=2, metavar=('ID', 'PRICE'), help="Обновить цену книги")
    parser.add_argument('--update-book-stock', nargs=2, metavar=('ID', 'STOCK'), help="Обновить остаток на складе")
    parser.add_argument('--update-order-status', nargs=2, metavar=('ID', 'STATUS'), help="Обновить статус заказа")
    parser.add_argument('--update-order-address', nargs=2, metavar=('ID', 'ADDRESS'), help="Обновить адрес заказа")
    
    parser.add_argument('--delete', nargs=2, type=str, metavar=('ENTITY', 'ID'), help="Удалить запись")
    
    args = parser.parse_args()
    
    if args.list:
        list_items(entity=args.list, fmt=args.fmt)
        
    elif args.create_author:
        create_named_entity("author", args.create_author, args.fmt)
    elif args.create_genre:
        create_named_entity("genre", args.create_genre, args.fmt)
    elif args.create_publisher:
        create_named_entity("publisher", args.create_publisher, args.fmt)
    elif args.create_customer:
        create_customer(name=args.create_customer[0], email=args.create_customer[1], fmt=args.fmt)
    elif args.create_book:
        create_book(*args.create_book, fmt=args.fmt)
    elif args.create_order:
        create_order(*args.create_order, fmt=args.fmt)
        
    elif args.update_name:
        update_name(entity=args.update_name[0], item_id=args.update_name[1], new_name=args.update_name[2], fmt=args.fmt)
    elif args.update_email:
        update_email(customer_id=args.update_email[0], new_email=args.update_email[1], fmt=args.fmt)
    elif args.update_book_title:
        update_book_field(args.update_book_title[0], "title", args.update_book_title[1], args.fmt)
    elif args.update_book_authors:
        update_book_field(args.update_book_authors[0], "authors", args.update_book_authors[1], args.fmt)
    elif args.update_book_publisher:
        update_book_field(args.update_book_publisher[0], "publisher", args.update_book_publisher[1], args.fmt)
    elif args.update_book_year:
        update_book_field(args.update_book_year[0], "year", args.update_book_year[1], args.fmt)
    elif args.update_book_genres:
        update_book_field(args.update_book_genres[0], "genres", args.update_book_genres[1], args.fmt)
    elif args.update_book_price:
        update_book_field(args.update_book_price[0], "price", args.update_book_price[1], args.fmt)
    elif args.update_book_stock:
        update_book_field(args.update_book_stock[0], "stock", args.update_book_stock[1], args.fmt)
    elif args.update_order_status:
        update_order_field(args.update_order_status[0], "status", args.update_order_status[1], args.fmt)
    elif args.update_order_address:
        update_order_field(args.update_order_address[0], "address", args.update_order_address[1], args.fmt)
        
    elif args.delete:
        delete_item(entity=args.delete[0], item_id=args.delete[1], fmt=args.fmt)
        
    else:
        parser.print_help()