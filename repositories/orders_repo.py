import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from models.orders import Order
from models.order_items import OrderItems
from core.exceptions import FormatFileError


# Репозиторий Order — CRUD-операции для JSON и XML
class OrderRepository:

    # Инициализация: путь к файлу и формат по расширению
    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    # READ: получить все заказы
    def get_all(self) -> list[Order]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    # CREATE: создать заказ (created_at = сейчас)
    def create_order(self, customer_id: int, items: list[OrderItems],
                     status: str, address: str, total: float) -> Order:
        order = Order(
            order_id=self._get_id(),
            customer_id=customer_id,
            items=items,
            status=status,
            created_at=datetime.now(),
            address=address,
            total=total,
        )
        orders = self.get_all()
        orders.append(order)
        self._save_all(orders)
        return order

    # READ: найти заказ по ID
    def find_order_by_id(self, order_id: int) -> Order | None:
        for order in self.get_all():
            if order.to_dict()["order_id"] == order_id:
                return order
        return None

    # DELETE: удалить заказ по ID
    def delete_order(self, order_id: int) -> bool:
        orders = self.get_all()
        for i, o in enumerate(orders):
            if o.to_dict()["order_id"] == order_id:
                orders.pop(i)
                self._save_all(orders)
                return True
        return False

    # UPDATE: изменить клиента
    def update_customer_id(self, order_id: int, customer_id: int) -> Order | None:
        return self._update_order(order_id, customer_id=customer_id)

    # UPDATE: изменить позиции (items → list[dict])
    def update_items(self, order_id: int, items: list[OrderItems]) -> Order | None:
        return self._update_order(
            order_id, items=[item.to_dict() for item in items]
        )

    # UPDATE: изменить статус
    def update_status(self, order_id: int, status: str) -> Order | None:
        return self._update_order(order_id, status=status)

    # UPDATE: изменить адрес
    def update_address(self, order_id: int, address: str) -> Order | None:
        return self._update_order(order_id, address=address)

    # UPDATE: изменить сумму
    def update_total(self, order_id: int, total: float) -> Order | None:
        return self._update_order(order_id, total=total)

    # UPDATE (общий): найти по ID и применить изменения
    def _update_order(self, order_id: int, **changes) -> Order | None:
        orders = self.get_all()
        for i, o in enumerate(orders):
            if o.to_dict()["order_id"] == order_id:
                data = o.to_dict()
                data.update(changes)
                updated = Order.from_dict(data)
                orders[i] = updated
                self._save_all(orders)
                return updated
        return None

    # WRITE: сохранить в зависимости от формата
    def _save_all(self, orders: list[Order]) -> None:
        if self._format == "json":
            self._write_json(orders)
        elif self._format == "xml":
            self._write_xml(orders)
        else:
            raise FormatFileError

    # READ (JSON): прочитать заказы из JSON
    def _read_json(self) -> list[Order]:
        with open(self._path, encoding="utf-8") as f:
            return [Order.from_dict(d) for d in json.load(f)]

    # READ (XML): прочитать заказы из XML (вложенные items)
    def _read_xml(self) -> list[Order]:
        tree = ET.parse(self._path)
        root = tree.getroot()
        orders = []
        for el in root.findall("./order"):
            items = []
            items_el = el.find("items")
            for item_el in items_el.findall("./item"):
                items.append(OrderItems.from_dict({
                    "product_id": int(item_el.findtext("product_id")),
                    "name": item_el.findtext("name"),
                    "price_at_purchase": float(item_el.findtext("price_at_purchase")),
                    "quantity": int(item_el.findtext("quantity")),
                }))
            orders.append(Order.from_dict({
                "order_id": int(el.findtext("order_id")),
                "customer_id": int(el.findtext("customer_id")),
                "items": [item.to_dict() for item in items],
                "status": el.findtext("status"),
                "created_at": el.findtext("created_at"),
                "address": el.findtext("address"),
                "total": float(el.findtext("total")),
            }))
        return orders

    # WRITE (JSON): записать заказы в JSON
    def _write_json(self, orders: list[Order]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in orders], f,
                      ensure_ascii=False, indent=2)

    # WRITE (XML): записать заказы в XML (вложенные items)
    def _write_xml(self, orders: list[Order]) -> None:
        root = ET.Element("orders")
        for o in orders:
            data = o.to_dict()
            el = ET.SubElement(root, "order")

            ET.SubElement(el, "order_id").text = str(data["order_id"])
            ET.SubElement(el, "customer_id").text = str(data["customer_id"])

            items_el = ET.SubElement(el, "items")
            for item in data["items"]:
                item_el = ET.SubElement(items_el, "item")
                ET.SubElement(item_el, "product_id").text = str(item["product_id"])
                ET.SubElement(item_el, "name").text = item["name"]
                ET.SubElement(item_el, "price_at_purchase").text = str(item["price_at_purchase"])
                ET.SubElement(item_el, "quantity").text = str(item["quantity"])

            ET.SubElement(el, "status").text = data["status"]
            ET.SubElement(el, "created_at").text = str(data.get("created_at") or "")
            ET.SubElement(el, "address").text = data["address"]
            ET.SubElement(el, "total").text = str(data["total"])

        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    # Следующий свободный ID (max + 1)
    def _get_id(self) -> int:
        orders = self.get_all()
        return max((o.to_dict()["order_id"] for o in orders), default=0) + 1