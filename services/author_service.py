from core.manager import Manager
from models.authors import Author
import re
from core.exceptions import AuthorNotFound, NameTypeError, IdTypeError
from core.validation_helper import ValidationHelper

class AuthorService:

    def __init__(self, db: Manager):
        self.db = db

    def create_author(self,name: str) -> Author:
        name = " ".join(name.split())
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        author = self.db.author.create_author(name)
        return author

    def get_author(self,author_id: str) -> Author:
        if not author_id.isdigit():
            raise IdTypeError
        author_id = int(author_id)
        author = self.db.author.find_author_by_id(author_id=author_id)
        if not author:
            raise AuthorNotFound
        return author

    def update_name(self,author_id: str, name: str) -> Author:
        name = " ".join(name.split())       
        if not author_id.isdigit() or int(author_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        author_id = int(author_id)
        author = self.db.author.update_author(author_id, name)
        if not author:
            raise AuthorNotFound
        return author

    def delete_author(self,author_id: str):
        if not author_id.isdigit():
            raise IdTypeError
        author_id = int(author_id)
        deleted = self.db.author.delete_author(author_id)
        if deleted:
            print(f"Удален автор {author_id}")
            return
        raise AuthorNotFound