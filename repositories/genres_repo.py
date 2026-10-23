import json
import xml.etree.ElementTree as ET
from pathlib import Path

from models.genres import Genre
from core.exceptions import FormatFileError


# Репозиторий Genre — CRUD-операции для JSON и XML
class GenreRepository:

    # Инициализация: путь к файлу и формат по расширению
    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    # READ: получить все жанры
    def get_all(self) -> list[Genre]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    # CREATE: создать жанр
    def create_genre(self, genre_name: str) -> Genre:
        genre = Genre(
            genre_id=self._get_id(),
            genre_name=genre_name,
        )
        genres = self.get_all()
        genres.append(genre)
        self._save_all(genres)
        return genre

    # READ: найти жанр по ID
    def find_genre_by_id(self, genre_id: int) -> Genre | None:
        for genre in self.get_all():
            if genre.to_dict()["genre_id"] == genre_id:
                return genre
        return None

    # DELETE: удалить жанр по ID
    def delete_genre(self, genre_id: int) -> bool:
        genres = self.get_all()
        for i, g in enumerate(genres):
            if g.to_dict()["genre_id"] == genre_id:
                genres.pop(i)
                self._save_all(genres)
                return True
        return False

    # UPDATE: изменить название жанра
    def update_genre_name(self, genre_id: int, genre_name: str) -> Genre | None:
        return self._update_genre(genre_id, genre_name=genre_name)

    # UPDATE (общий): найти по ID и применить изменения
    def _update_genre(self, genre_id: int, **changes) -> Genre | None:
        genres = self.get_all()
        for i, g in enumerate(genres):
            if g.to_dict()["genre_id"] == genre_id:
                data = g.to_dict()
                data.update(changes)
                updated = Genre.from_dict(data)
                genres[i] = updated
                self._save_all(genres)
                return updated
        return None

    # WRITE: сохранить в зависимости от формата
    def _save_all(self, genres: list[Genre]) -> None:
        if self._format == "json":
            self._write_json(genres)
        elif self._format == "xml":
            self._write_xml(genres)
        else:
            raise FormatFileError

    # READ (JSON): прочитать жанры из JSON
    def _read_json(self) -> list[Genre]:
        with open(self._path, encoding="utf-8") as f:
            return [Genre.from_dict(d) for d in json.load(f)]

    # READ (XML): прочитать жанры из XML
    def _read_xml(self) -> list[Genre]:
        tree = ET.parse(self._path)
        root = tree.getroot()
        genres = []
        for el in root.findall("./genre"):
            genres.append(Genre.from_dict({
                "genre_id": int(el.findtext("genre_id")),
                "genre_name": el.findtext("genre_name"),
            }))
        return genres

    # WRITE (JSON): записать жанры в JSON
    def _write_json(self, genres: list[Genre]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([g.to_dict() for g in genres], f,
                      ensure_ascii=False, indent=2)

    # WRITE (XML): записать жанры в XML
    def _write_xml(self, genres: list[Genre]) -> None:
        root = ET.Element("genres")
        for g in genres:
            data = g.to_dict()
            el = ET.SubElement(root, "genre")
            ET.SubElement(el, "genre_id").text = str(data["genre_id"])
            ET.SubElement(el, "genre_name").text = data["genre_name"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    # Следующий свободный ID (max + 1)
    def _get_id(self) -> int:
        genres = self.get_all()
        return max((g.to_dict()["genre_id"] for g in genres), default=0) + 1