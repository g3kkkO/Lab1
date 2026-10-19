from datetime import datetime
from models.order_items import OrderItems


class Order:

    def __init__(self, order_id: int, customer_id: int,
                 items: list[OrderItems], status: str, created_at: datetime,
                 address: str, total: float):
        self._order_id = order_id
        self._customer_id = customer_id
        self._items = items
        self._status = status
        self._created_at = created_at
        self._address = address
        self._total = total

    def to_dict(self) -> dict:
        return {
            "order_id": self._order_id,
            "customer_id": self._customer_id,
            "items": [item.to_dict() for item in self._items],
            "status": self._status,
            "created_at": self._created_at.isoformat(),
            "address": self._address,
            "total": self._total,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            items=[OrderItems.from_dict(d) for d in data["items"]],
            status=data["status"],
            created_at=datetime.fromisoformat(data["created_at"]),
            address=data["address"],
            total=data["total"],
        )