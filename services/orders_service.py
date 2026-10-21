from core.manager import Manager
from core.exceptions import (IdTypeError, NameTypeError, BookNotFound,
                              OrderNotFound, StatusValueError, YearValueError)
from core.validation_helper import ValidationHelper
from models.orders import Order
from models.order_items import OrderItems


# Сервис Order — бизнес-логика и валидация для CRUD
class OrderService:

    # Допустимые статусы заказа
    VALID_STATUSES = {"new", "paid", "shipped", "delivered", "cancelled"}

    # Инициализация: менеджер репозиториев
    def __init__(self, db: Manager):
        self.db = db

    # READ: получить все заказы
    def get_all(self) -> list[Order]:
        return self.db.order.get_all()

    # CREATE: создать заказ (валидация клиента, адреса, статуса, позиций)
    def create_order(self, customer_id: str, items: list[dict],
                     status: str, address: str) -> Order:
        if not customer_id.isdigit() or int(customer_id) <= 0:
            raise IdTypeError
        address = " ".join(address.split())
        if not ValidationHelper.validate_name(address):
            raise NameTypeError
        status = status.strip().lower()
        if status not in self.VALID_STATUSES:
            raise StatusValueError

        order_items = []
        total = 0.0
        for it in items:
            product_id = str(it["product_id"]).strip()
            if not product_id.isdigit() or int(product_id) <= 0:
                raise IdTypeError
            quantity = str(it.get("quantity", 1)).strip()
            if not quantity.isdigit() or int(quantity) <= 0:
                raise IdTypeError

            book = self.db.book.find_book_by_id(book_id=int(product_id))
            if not book:
                raise BookNotFound

            data = book.to_dict()
            price = float(data["price"])
            qty = int(quantity)
            order_items.append(OrderItems(
                product_id=int(product_id),
                name=data["title"],
                price_at_purchase=price,
                quantity=qty,
            ))
            total += price * qty

        return self.db.order.create_order(
            customer_id=int(customer_id),
            items=order_items,
            status=status,
            address=address,
            total=total,
        )

    # READ: найти заказ по ID
    def get_order(self, order_id: str) -> Order:
        if not order_id.isdigit() or int(order_id) <= 0:
            raise IdTypeError
        order = self.db.order.find_order_by_id(order_id=int(order_id))
        if not order:
            raise OrderNotFound
        return order

    # UPDATE: изменить статус
    def update_status(self, order_id: str, status: str) -> Order:
        if not order_id.isdigit() or int(order_id) <= 0:
            raise IdTypeError
        status = status.strip().lower()
        if status not in self.VALID_STATUSES:
            raise StatusValueError
        updated = self.db.order.update_status(int(order_id), status)
        if not updated:
            raise OrderNotFound
        return updated

    # UPDATE: изменить адрес
    def update_address(self, order_id: str, address: str) -> Order:
        if not order_id.isdigit() or int(order_id) <= 0:
            raise IdTypeError
        updated = self.db.order.update_address(int(order_id), address)
        if not updated:
            raise OrderNotFound
        return updated

    # DELETE: удалить заказ по ID
    def delete_order(self, order_id: str) -> None:
        if not order_id.isdigit() or int(order_id) <= 0:
            raise IdTypeError
        deleted = self.db.order.delete_order(int(order_id))
        if deleted:
            print(f"Удалён заказ {order_id}")
            return
        raise OrderNotFound