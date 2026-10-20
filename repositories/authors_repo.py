import json
import xml.etree.ElementTree as ET
from pathlib import Path
from models.authors import Author
from exceptions.FormatException import FormatFileError



class AuthorRepository:

    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()
        

    def get_all(self) -> list[Author]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError

    def create_author(self, name: str) -> Author:
        if self._format == "json":
            return self._create_author_json(name)
        if self._format == "xml":
            return self._create_author_xml(name)
        raise FormatFileError
    
    def update_author(self, author_id: int,name: str) -> Author | None:
        if self._format == "json":
            return self._update_name_json(author_id,name)
        if self._format == "xml":
            return self._update_name_xml(author_id,name)
        raise FormatFileError
    
    def find_author_by_id(self, author_id: int) -> Author | None:
        for author in self.get_all():
            if author.to_dict()["author_id"] == author_id:
                return author
        return None

    def delete_author(self, author_id: int) -> bool:
        if self._format == "json":
            return self._delete_author_json(author_id)
        if self._format == "xml":
            return self._delete_author_xml(author_id)
        raise FormatFileError
    
    def _create_author_json(self, name: str) -> Author:
        author = Author(author_id=self._get_id(), name=name)
        authors = self.get_all()          
        authors.append(author)            
        self._write_json(authors)    
        return author

    def _create_author_xml(self, name: str) -> Author:
        author = Author(author_id=self._get_id(), name=name)
        authors = self.get_all()          
        authors.append(author)            
        self._write_xml(authors)    
        return author

    def _read_json(self) -> list[Author]:
        with open(self._path, encoding="utf-8") as f:
            return [Author.from_dict(d) for d in json.load(f)]

    def _read_xml(self) -> list[Author]:
        tree = ET.parse(self._path)
        authors = []
        root = tree.getroot()
        for author in root.findall('./author'):
            author_id = int(author.findtext('author_id'))
            name = author.findtext('name')
            authors.append(Author(author_id=author_id,name=name))
        return authors

    def _update_name_json(self, author_id: int, name: str) -> Author | None:
        authors = self.get_all()
        for i, author in enumerate(authors):
            if author.to_dict()["author_id"] == author_id:
                updated = Author(author_id=author_id, name=name)  
                authors[i] = updated
                self._write_json(authors)
                return updated
        return None

    def _update_name_xml(self, author_id: int, name: str) -> Author | None:
        authors = self.get_all()
        for i, author in enumerate(authors):
            if author.to_dict()["author_id"] == author_id:
                updated = Author(author_id=author_id, name=name)  
                authors[i] = updated
                self._write_xml(authors)
                return updated
        return None

    def _write_json(self, authors: list[Author]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in authors], f, ensure_ascii=False, indent=2)
  
    def _write_xml(self, authors: list[Author]) -> None:
        root = ET.Element("authors")
        for a in authors:
            data = a.to_dict()
            el = ET.SubElement(root, "author")
            ET.SubElement(el, "author_id").text = str(data["author_id"])
            ET.SubElement(el, "name").text = data["name"]
        ET.indent(root)
        ET.ElementTree(root).write(self._path, encoding="utf-8", xml_declaration=True)
    
    def _delete_author_json(self, author_id: int) -> bool:
        authors = self.get_all()
        for i, author in enumerate(authors):
            if author.to_dict()["author_id"] == author_id:
                authors.pop(i)
                self._write_json(authors)
                return True
        return False

    def _delete_author_xml(self, author_id: int) -> bool:
        authors = self.get_all()
        for i, author in enumerate(authors):
            if author.to_dict()["author_id"] == author_id:
                authors.pop(i)
                self._write_xml(authors)
                return True
        return False

    def _get_id(self) -> int:
        items = self.get_all()
        return max((item.to_dict()["author_id"] for item in items), default=0) + 1
    

