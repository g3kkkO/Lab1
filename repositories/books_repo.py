import json
import xml.etree.ElementTree as ET
from pathlib import Path
from models.books import Book
from core.exceptions import FormatFileError

class BookRepository:

    def __init__(self, path: str):
        self._path = Path(path)
        self._format = self._path.suffix.lstrip(".").lower()

    def get_all(self) -> list[Book]:
        if self._format == "json":
            return self._read_json()
        if self._format == "xml":
            return self._read_xml()
        raise FormatFileError
    
    def create_book(self, title: str, author_ids: list[int], publisher_id: int,
                    year: int, genres_ids: list[int], price: float, stock: int) -> Book:
        book = Book(book_id=self._get_id(), title=title, author_ids=author_ids,
                    publisher_id=publisher_id, year=year, genres_ids=genres_ids,
                    price=price, stock=stock)
        books = self.get_all()
        books.append(book)
        self._save_all(books)
        return book

    def find_book_by_id(self, book_id: int) -> Book | None:
        for book in self.get_all():
            if book.to_dict()["book_id"] == book_id:
                return book
        return None

    def delete_book(self, book_id: int) -> bool:
        books = self.get_all()
        for i, b in enumerate(books):
            if b.to_dict()["book_id"] == book_id:
                books.pop(i)
                self._save_all(books)
                return True
        return False

    def update_title(self, book_id: int, title: str) -> Book | None:
        return self._update_book(book_id, title=title)

    def update_author_ids(self, book_id: int, author_ids: list[int]) -> Book | None:
        return self._update_book(book_id, author_ids=author_ids)

    def update_publisher_id(self, book_id: int, publisher_id: int) -> Book | None:
        return self._update_book(book_id, publisher_id=publisher_id)

    def update_year(self, book_id: int, year: int) -> Book | None:
        return self._update_book(book_id, year=year)

    def update_genres(self, book_id: int, genres_ids: list[int]) -> Book | None:
        return self._update_book(book_id, genres_ids=genres_ids)

    def update_price(self, book_id: int, price: float) -> Book | None:
        return self._update_book(book_id, price=price)

    def update_stock(self, book_id: int, stock: int) -> Book | None:
        return self._update_book(book_id, stock=stock)

    def _update_book(self, book_id: int, **changes) -> Book | None:
        books = self.get_all()
        for i, b in enumerate(books):
            if b.to_dict()["book_id"] == book_id:
                data = b.to_dict()
                data.update(changes)                 
                updated = Book.from_dict(data)       
                books[i] = updated
                self._save_all(books)
                return updated
        return None

    def _save_all(self, books: list[Book]) -> None:
        if self._format == "json":
            self._write_json(books)
        elif self._format == "xml":
            self._write_xml(books)
        else:
            raise ValueError(f"Неподдерживаемый формат: {self._format}")

    def _read_json(self) -> list[Book]:
        with open(self._path, encoding="utf-8") as f:
            return [Book.from_dict(d) for d in json.load(f)]

    def _read_xml(self) -> list[Book]:
        tree = ET.parse(self._path)
        root = tree.getroot()
        books = []
        for el in root.findall("./book"):
            author_ids = [int(x.text) for x in el.find("author_ids").findall("id")]
            genres_ids = [int(x.text) for x in el.find("genres_ids").findall("id")]
            books.append(Book.from_dict({
                "book_id": int(el.findtext("book_id")),
                "title": el.findtext("title"),
                "author_ids": author_ids,
                "publisher_id": int(el.findtext("publisher_id")),
                "year": int(el.findtext("year")),
                "genres_ids": genres_ids,
                "price": float(el.findtext("price")),
                "stock": int(el.findtext("stock")),
            }))
        return books

    def _write_json(self, books: list[Book]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in books], f,
                      ensure_ascii=False, indent=2)

    def _write_xml(self, books: list[Book]) -> None:
        root = ET.Element("books")
        for b in books:
            data = b.to_dict()
            el = ET.SubElement(root, "book")

            ET.SubElement(el, "book_id").text = str(data["book_id"])
            ET.SubElement(el, "title").text = data["title"]

            author_ids_el = ET.SubElement(el, "author_ids")
            for aid in data["author_ids"]:
                ET.SubElement(author_ids_el, "id").text = str(aid)

            ET.SubElement(el, "publisher_id").text = str(data["publisher_id"])
            ET.SubElement(el, "year").text = str(data["year"])

            genres_el = ET.SubElement(el, "genres_ids")
            for gid in data["genres_ids"]:
                ET.SubElement(genres_el, "id").text = str(gid)

            ET.SubElement(el, "price").text = str(data["price"])
            ET.SubElement(el, "stock").text = str(data["stock"])

        ET.indent(root)
        ET.ElementTree(root).write(self._path,
                                   encoding="utf-8", xml_declaration=True)

    def _get_id(self) -> int:
        books = self.get_all()
        return max((b.to_dict()["book_id"] for b in books), default=0) + 1