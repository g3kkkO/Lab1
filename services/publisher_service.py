from core.manager import Manager
from core.exceptions import PublisherNotFound, NameTypeError, IdTypeError
from models.publishers import Publisher
from core.validation_helper import ValidationHelper

class PublisherService:

    def __init__(self, db: Manager):
            self.db = db

    def create_publisher(self, name: str) -> Publisher:
        name = " ".join(name.split())
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        publisher = self.db.publisher.create_publisher(name)
        return publisher

    def get_publisher(self,publisher_id: str) -> Publisher:
        if not publisher_id.isdigit() or int(publisher_id) <= 0:
            raise IdTypeError
        publisher_id = int(publisher_id)
        publisher = self.db.publisher.find_publisher_by_id(publisher_id=publisher_id)
        if not publisher:
            raise PublisherNotFound
        return publisher

    def update_name(self, publisher_id: str, name: str) -> Publisher:
        name = " ".join(name.split())
        if not publisher_id.isdigit() or int(publisher_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        updated = self.db.publisher.update_name(int(publisher_id), name)
        if not updated:
            raise PublisherNotFound
        return updated

    def delete_publisher(self,publisher_id: str) -> None:
        if not publisher_id.isdigit() or int(publisher_id) <= 0:
            raise IdTypeError
        publisher_id = int(publisher_id)
        deleted = self.db.publisher.delete_publisher(publisher_id)
        if deleted:
            print(f"Удалено издание {publisher_id}")
            return
        raise PublisherNotFound