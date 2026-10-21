import json
import xml.etree.ElementTree as ET
from pathlib import Path

from models.customers import Customer
from core.exceptions import FormatFileError


# Репозиторий Customer — CRUD-операции для JSON и XML
class CustomerRepository:

    # Инициализация: путь к файлу и формат по расширению
    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    # READ: получить всех клиентов
    def get_all(self) -> list[Customer]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    # CREATE: создать клиента
    def create_customer(self, name: str, email: str) -> Customer:
        customer = Customer(
            customer_id=self._get_id(),
            name=name,
            email=email,
        )
        customers = self.get_all()
        customers.append(customer)
        self._save_all(customers)
        return customer

    # READ: найти клиента по ID
    def find_customer_by_id(self, customer_id: int) -> Customer | None:
        for customer in self.get_all():
            if customer.to_dict()["customer_id"] == customer_id:
                return customer
        return None

    # DELETE: удалить клиента по ID
    def delete_customer(self, customer_id: int) -> bool:
        customers = self.get_all()
        for i, c in enumerate(customers):
            if c.to_dict()["customer_id"] == customer_id:
                customers.pop(i)
                self._save_all(customers)
                return True
        return False

    # UPDATE: изменить имя
    def update_name(self, customer_id: int, name: str) -> Customer | None:
        return self._update_customer(customer_id, name=name)

    # UPDATE: изменить email
    def update_email(self, customer_id: int, email: str) -> Customer | None:
        return self._update_customer(customer_id, email=email)

    # UPDATE (общий): найти по ID и применить изменения
    def _update_customer(self, customer_id: int, **changes) -> Customer | None:
        customers = self.get_all()
        for i, c in enumerate(customers):
            if c.to_dict()["customer_id"] == customer_id:
                data = c.to_dict()
                data.update(changes)
                updated = Customer.from_dict(data)
                customers[i] = updated
                self._save_all(customers)
                return updated
        return None

    # WRITE: сохранить в зависимости от формата
    def _save_all(self, customers: list[Customer]) -> None:
        if self._format == "json":
            self._write_json(customers)
        elif self._format == "xml":
            self._write_xml(customers)
        else:
            raise FormatFileError

    # READ (JSON): прочитать клиентов из JSON
    def _read_json(self) -> list[Customer]:
        with open(self._path, encoding="utf-8") as f:
            return [Customer.from_dict(d) for d in json.load(f)]

    # READ (XML): прочитать клиентов из XML
    def _read_xml(self) -> list[Customer]:
        tree = ET.parse(self._path)
        root = tree.getroot()
        customers = []
        for el in root.findall("./customer"):
            customers.append(Customer.from_dict({
                "customer_id": int(el.findtext("customer_id")),
                "name": el.findtext("name"),
                "email": el.findtext("email"),
            }))
        return customers

    # WRITE (JSON): записать клиентов в JSON
    def _write_json(self, customers: list[Customer]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in customers], f,
                      ensure_ascii=False, indent=2)

    # WRITE (XML): записать клиентов в XML
    def _write_xml(self, customers: list[Customer]) -> None:
        root = ET.Element("customers")
        for c in customers:
            data = c.to_dict()
            el = ET.SubElement(root, "customer")
            ET.SubElement(el, "customer_id").text = str(data["customer_id"])
            ET.SubElement(el, "name").text = data["name"]
            ET.SubElement(el, "email").text = data["email"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    # Следующий свободный ID (max + 1)
    def _get_id(self) -> int:
        customers = self.get_all()
        return max((c.to_dict()["customer_id"] for c in customers), default=0) + 1