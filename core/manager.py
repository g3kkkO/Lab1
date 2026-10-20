from repositories.authors_repo import AuthorRepository
from repositories.books_repo import BookRepository
from repositories.customer_repo import CustomerRepository
from repositories.genres_repo import GenreRepository
from repositories.orders_repo import OrderRepository
from repositories.publisher_repo import PublisherRepository

class Manager:

    def __init__(self, path):
        self.path = path
        self.author = AuthorRepository(path=path)
        self.book = BookRepository(path=path)
        self.customer = CustomerRepository(path=path)
        self.genre = GenreRepository(path=path)
        self.order = OrderRepository(path=path)
        self.publisher = PublisherRepository(path=path)
