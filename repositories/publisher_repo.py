import json
import xml.etree.ElementTree as ET
from pathlib import Path
from models.publishers import Publisher
from exceptions.FormatException import FormatFileError


class PublisherRepository:

    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    def get_all(self) -> list[Publisher]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError
    
    def create_publisher(self, name: str, contact: str) -> Publisher:
        publisher = Publisher(publisher_id=self._get_id(), name=name, contact=contact)
        publishers = self.get_all()
        publishers.append(publisher)
        self._save_all(publishers)
        return publisher

    def find_publisher_by_id(self, publisher_id: int) -> Publisher | None:
        for publisher in self.get_all():
            if publisher.to_dict()["publisher_id"] == publisher_id:
                return publisher
        return None

    def delete_publisher(self, publisher_id: int) -> bool:
        publishers = self.get_all()
        for i, p in enumerate(publishers):
            if p.to_dict()["publisher_id"] == publisher_id:
                publishers.pop(i)
                self._save_all(publishers)
                return True
        return False

    def update_name(self, publisher_id: int, name: str) -> Publisher | None:
        return self._update_publisher(publisher_id, name=name)

    def update_contact(self, publisher_id: int, contact: str) -> Publisher | None:
        return self._update_publisher(publisher_id, contact=contact)

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

    def _save_all(self, publishers: list[Publisher]) -> None:
        if self._format == "json":
            self._write_json(publishers)
        elif self._format == "xml":
            self._write_xml(publishers)
        else:
            raise FormatFileError

    def _read_json(self) -> list[Publisher]:
        with open(self._path, encoding="utf-8") as f:
            return [Publisher.from_dict(d) for d in json.load(f)]

    def _read_xml(self) -> list[Publisher]:
        root = ET.parse(self._path).getroot()
        return [
            Publisher.from_dict({
                "publisher_id": int(el.findtext("publisher_id")),
                "name": el.findtext("name"),
                "contact": el.findtext("contact"),
            })
            for el in root.findall("./publisher")
        ]

    def _write_json(self, publishers: list[Publisher]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in publishers], f,
                      ensure_ascii=False, indent=2)

    def _write_xml(self, publishers: list[Publisher]) -> None:
        root = ET.Element("publishers")
        for p in publishers:
            data = p.to_dict()
            el = ET.SubElement(root, "publisher")
            ET.SubElement(el, "publisher_id").text = str(data["publisher_id"])
            ET.SubElement(el, "name").text = data["name"]
            ET.SubElement(el, "contact").text = data["contact"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    def _get_id(self) -> int:
        publishers = self.get_all()
        return max((p.to_dict()["publisher_id"] for p in publishers), default=0) + 1