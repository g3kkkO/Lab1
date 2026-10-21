from core.manager import Manager
from models.authors import Author
import re
from core.exceptions import AuthorNotFound, NameTypeError, IdTypeError
from core.validation_helper import ValidationHelper


# Сервис Author — бизнес-логика и валидация для CRUD
class AuthorService:

    # Инициализация: менеджер репозиториев
    def __init__(self, db: Manager):
        self.db = db

    # CREATE: создать автора (с валидацией имени)
    def create_author(self, name: str) -> Author:
        name = " ".join(name.split())
        if not ValidationHelper.validate_name(name):
            raise NameTypeError
        author = self.db.author.create_author(name)
        return author

    # READ: получить всех авторов
    def get_all(self) -> list[Author]:
        return self.db.author.get_all()

    # READ: найти автора по ID (с валидацией ID)
    def get_author(self, author_id: str) -> Author:
        if not author_id.isdigit():
            raise IdTypeError
        author_id = int(author_id)
        author = self.db.author.find_author_by_id(author_id=author_id)
        if not author:
            raise AuthorNotFound
        return author

    # UPDATE: изменить имя автора (валидация ID и имени)
    def update_name(self, author_id: str, name: str) -> Author:
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

    # DELETE: удалить автора по ID
    def delete_author(self, author_id: str):
        if not author_id.isdigit():
            raise IdTypeError
        author_id = int(author_id)
        deleted = self.db.author.delete_author(author_id)
        if deleted:
            print(f"Удален автор {author_id}")
            return
        raise AuthorNotFound