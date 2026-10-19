class OrderItems:

    def __init__(self, product_id: int, name: str,
                 price_at_purchase: float, quantity: int = 1):
        self._product_id = product_id
        self._name = name
        self._price_at_purchase = price_at_purchase
        self._quantity = quantity

    def total(self) -> float:
        return self._price_at_purchase * self._quantity

    def to_dict(self) -> dict:
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price_at_purchase": self._price_at_purchase,
            "quantity": self._quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OrderItems":
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price_at_purchase=data["price_at_purchase"],
            quantity=data.get("quantity", 1),
        )