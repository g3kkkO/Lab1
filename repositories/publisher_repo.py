import json
import xml.etree.ElementTree as ET
from pathlib import Path
from models.publishers import Publisher
from core.exceptions import FormatFileError


# Репозиторий Publisher — CRUD-операции для JSON и XML
class PublisherRepository:

    # Инициализация: путь к файлу и формат по расширению
    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    # READ: получить всех издателей
    def get_all(self) -> list[Publisher]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    # CREATE: создать издателя
    def create_publisher(self, publisher_name: str) -> Publisher:
        publisher = Publisher(publisher_id=self._get_id(), publisher_name=publisher_name)
        publishers = self.get_all()
        publishers.append(publisher)
        self._save_all(publishers)
        return publisher

    # READ: найти издателя по ID
    def find_publisher_by_id(self, publisher_id: int) -> Publisher | None:
        for publisher in self.get_all():
            if publisher.to_dict()["publisher_id"] == publisher_id:
                return publisher
        return None

    # DELETE: удалить издателя по ID
    def delete_publisher(self, publisher_id: int) -> bool:
        publishers = self.get_all()
        for i, p in enumerate(publishers):
            if p.to_dict()["publisher_id"] == publisher_id:
                publishers.pop(i)
                self._save_all(publishers)
                return True
        return False

    # UPDATE: изменить название
    def update_name(self, publisher_id: int, publisher_name: str) -> Publisher | None:
        return self._update_publisher(publisher_id, publisher_name=publisher_name)

    # UPDATE (общий): найти по ID и применить изменения
    def _update_publisher(self, publisher_id: int, **changes) -> Publisher | None:
        publishers = self.get_all()
        for i, p in enumerate(publishers):
            if p.to_dict()["publisher_id"] == publisher_id:
                data = p.to_dict()
                data.update(changes)
                updated = Publisher.from_dict(data)
                publishers[i] = updated
                self._save_all(publishers)
                return updated
        return None

    # WRITE: сохранить в зависимости от формата
    def _save_all(self, publishers: list[Publisher]) -> None:
        if self._format == "json":
            self._write_json(publishers)
        elif self._format == "xml":
            self._write_xml(publishers)
        else:
            raise FormatFileError

    # READ (JSON): прочитать издателей из JSON
    def _read_json(self) -> list[Publisher]:
        with open(self._path, encoding="utf-8") as f:
            return [Publisher.from_dict(d) for d in json.load(f)]

    # READ (XML): прочитать издателей из XML
    def _read_xml(self) -> list[Publisher]:
        root = ET.parse(self._path).getroot()
        return [
            Publisher.from_dict({
                "publisher_id": int(el.findtext("publisher_id")),
                "publisher_name": el.findtext("publisher_name"),
            })
            for el in root.findall("./publisher")
        ]

    # WRITE (JSON): записать издателей в JSON
    def _write_json(self, publishers: list[Publisher]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in publishers], f,
                      ensure_ascii=False, indent=2)

    # WRITE (XML): записать издателей в XML
    def _write_xml(self, publishers: list[Publisher]) -> None:
        root = ET.Element("publishers")
        for p in publishers:
            data = p.to_dict()
            el = ET.SubElement(root, "publisher")
            ET.SubElement(el, "publisher_id").text = str(data["publisher_id"])
            ET.SubElement(el, "publisher_name").text = data["publisher_name"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    # Следующий свободный ID (max + 1)
    def _get_id(self) -> int:
        publishers = self.get_all()
        return max((p.to_dict()["publisher_id"] for p in publishers), default=0) + 1