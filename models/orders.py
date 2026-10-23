from models.order_items import OrderItems


from datetime import datetime


# Класс-модель Order
class Order:

    def __init__(self, order_id: int, customer_id: int,
                 items: list[OrderItems], status: str,
                 address: str, total: float, created_at=None):
        self._order_id = order_id
        self._customer_id = customer_id
        self._items = items
        self._status = status
        self._address = address
        self._total = total
        self._created_at = created_at

    # Преобразование объекта в словарь
    def to_dict(self) -> dict:
        created_at = self._created_at
        if hasattr(created_at, "isoformat"):
            created_at = created_at.isoformat()

        return {
            "order_id": self._order_id,
            "customer_id": self._customer_id,
            "items": [item.to_dict() for item in self._items],
            "status": self._status,
            "address": self._address,
            "total": self._total,
            "created_at": created_at,
        }

    # Создание объекта из словаря 
    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = None

        return cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            items=[OrderItems.from_dict(d) for d in data["items"]],
            status=data["status"],
            address=data["address"],
            total=data["total"],
            created_at=created_at,
        )