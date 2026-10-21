from models.order_items import OrderItems


# Класс-модель Order
class Order:

    def __init__(self, order_id: int, customer_id: int,
                 items: list[OrderItems], status: str,
                 address: str, total: float):
        self._order_id = order_id
        self._customer_id = customer_id
        self._items = items
        self._status = status
        self._address = address
        self._total = total

    # Преобразование объекта в словарь
    def to_dict(self) -> dict:
        return {
            "order_id": self._order_id,
            "customer_id": self._customer_id,
            "items": [item.to_dict() for item in self._items],
            "status": self._status,
            "address": self._address,
            "total": self._total,
        }

    # Создание объекта из словаря 
    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            items=[OrderItems.from_dict(d) for d in data["items"]],
            status=data["status"],
            address=data["address"],
            total=data["total"],
        )