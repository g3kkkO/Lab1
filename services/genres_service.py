from core.manager import Manager
from core.exceptions import GenreNotFound, NameTypeError, IdTypeError
from models.genres import Genre
from core.validation_helper import ValidationHelper



class GenreService:

    def __init__(self, db: Manager):
        self.db = db

    def create_genre(self, genre_name: str) -> Genre:
        genre_name = " ".join(genre_name.split())
        if not ValidationHelper.validate_name(genre_name):
            raise NameTypeError
        genre = self.db.genre.create_genre(genre_name)
        return genre

    def get_genre(self,genre_id: str) -> Genre:
        if not genre_id.isdigit() or int(genre_id) <= 0:
            raise IdTypeError
        genre_id = int(genre_id)
        genre = self.db.genre.find_genre_by_id(genre_id=genre_id)
        if not genre:
            raise GenreNotFound
        return genre

    def get_all(self) -> list[Genre]:
        return self.db.genre.get_all()

    def update_name(self, genre_id: str, genre_name: str) -> Genre:
        genre_name = " ".join(genre_name.split())
        if not genre_id.isdigit() or int(genre_id) <= 0:
            raise IdTypeError
        if not ValidationHelper.validate_name(genre_name):
            raise NameTypeError
        updated = self.db.genre.update_genre_name(int(genre_id), genre_name)
        if not updated:
            raise GenreNotFound
        return updated

    def delete_genre(self,genre_id: str) -> None:
        if not genre_id.isdigit() or int(genre_id) <= 0:
            raise IdTypeError
        genre_id = int(genre_id)
        deleted = self.db.genre.delete_genre(genre_id)
        if deleted:
            print(f"Удален жанр {genre_id}")
            return
        raise GenreNotFound