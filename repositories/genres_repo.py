import json
import xml.etree.ElementTree as ET
from pathlib import Path

from models.genres import Genre
from exceptions.FormatException import FormatFileError


class GenreRepository:

    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    def get_all(self) -> list[Genre]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    def create_genre(self, genre_name: str) -> Genre:
        genre = Genre(
            genres_id=self._get_id(),
            genre_name=genre_name,
        )
        genres = self.get_all()
        genres.append(genre)
        self._save_all(genres)
        return genre

    def find_genre_by_id(self, genres_id: int) -> Genre | None:
        for genre in self.get_all():
            if genre.to_dict()["genres_id"] == genres_id:
                return genre
        return None

    def delete_genre(self, genres_id: int) -> bool:
        genres = self.get_all()
        for i, g in enumerate(genres):
            if g.to_dict()["genres_id"] == genres_id:
                genres.pop(i)
                self._save_all(genres)
                return True
        return False

    def update_genre_name(self, genres_id: int, genre_name: str) -> Genre | None:
        return self._update_genre(genres_id, genre_name=genre_name)

    def _update_genre(self, genres_id: int, **changes) -> Genre | None:
        genres = self.get_all()
        for i, g in enumerate(genres):
            if g.to_dict()["genres_id"] == genres_id:
                data = g.to_dict()
                data.update(changes)
                updated = Genre.from_dict(data)
                genres[i] = updated
                self._save_all(genres)
                return updated
        return None

    def _save_all(self, genres: list[Genre]) -> None:
        if self._format == "json":
            self._write_json(genres)
        elif self._format == "xml":
            self._write_xml(genres)
        else:
            raise FormatFileError

    def _read_json(self) -> list[Genre]:
        with open(self._path, encoding="utf-8") as f:
            return [Genre.from_dict(d) for d in json.load(f)]

    def _read_xml(self) -> list[Genre]:
        tree = ET.parse(self._path)
        root = tree.getroot()
        genres = []
        for el in root.findall("./genre"):
            genres.append(Genre.from_dict({
                "genres_id": int(el.findtext("genres_id")),
                "genre_name": el.findtext("genre_name"),
            }))
        return genres

    def _write_json(self, genres: list[Genre]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([g.to_dict() for g in genres], f,
                      ensure_ascii=False, indent=2)

    def _write_xml(self, genres: list[Genre]) -> None:
        root = ET.Element("genres")
        for g in genres:
            data = g.to_dict()
            el = ET.SubElement(root, "genre")
            ET.SubElement(el, "genres_id").text = str(data["genres_id"])
            ET.SubElement(el, "genre_name").text = data["genre_name"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    def _get_id(self) -> int:
        genres = self.get_all()
        return max((g.to_dict()["genres_id"] for g in genres), default=0) + 1