from core.manager import Manager
from core.exceptions import CustomerNotFound, NameTypeError, IdTypeError, InvalidEmailError
from models.customers import Customer
from core.validation_helper import ValidationHelper



class CustomerService:

    def __init__(self, db: Manager):
        self.db = db

    def create_customer(self, customer_name: str, email: str) -> Customer:
        customer_name = " ".join(customer_name.split())
        if not ValidationHelper.validate_name(customer_name):
            raise NameTypeError
        if not ValidationHelper.validate_email(email):
            raise InvalidEmailError
        customer = self.db.customer.create_customer(customer_name,email)
        return customer
    
    def get_all(self) -> list[Customer]:
        return self.db.customer.get_all()

    def get_customer(self,customer_id: str) -> Customer:
        if not customer_id.isdigit() or int(customer_id) <= 0:
            raise IdTypeError
        customer_id = int(customer_id)
        customer = self.db.customer.find_customer_by_id(customer_id=customer_id)
        if not customer:
            raise CustomerNotFound
        return customer

    def update_name(self, customer_id: str, name: str) -> Customer:
        name = " ".join(name.split())
        if not customer_id.isdigit() or int(customer_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        updated = self.db.customer.update_name(int(customer_id), name)
        if not updated:
            raise CustomerNotFound
        return updated

    def update_email(self, customer_id: str, email: str) -> Customer:
        if not customer_id.isdigit() or int(customer_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_email(email):
            raise InvalidEmailError
        updated = self.db.customer.update_email(int(customer_id), email)
        if not updated:
            raise CustomerNotFound
        return updated

    def delete_customer(self,customer_id: str) -> None:
        if not customer_id.isdigit() or int(customer_id) <= 0:
            raise IdTypeError
        customer_id = int(customer_id)
        deleted = self.db.customer.delete_customer(customer_id)
        if deleted:
            print(f"Удален покупатель {customer_id}")
            return
        raise CustomerNotFound