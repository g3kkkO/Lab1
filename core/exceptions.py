class FormatFileError(Exception):
    def __init__(self, message="Расширение файла должно быть json или xml"):
        super().__init__(message)

class AuthorNotFound(Exception):
    def __init__(self, message="Автор не найден"):
        super().__init__(message)

class IdTypeError(Exception):
    def __init__(self, message="Id должен содержать только числа"):
        super().__init__(message)

class NameTypeError(Exception):
    def __init__(self, message="Ошибка в записи имени"):
        super().__init__(message)


class PublisherNotFound(Exception):
    def __init__(self, message="Издание не найдено"):
        super().__init__(message)

class GenreNotFound(Exception):
    def __init__(self, message="Жанр не найден"):
        super().__init__(message)


class CustomerNotFound(Exception):
    def __init__(self, message="Покупатель не найден"):
        super().__init__(message) 

class InvalidEmailError(Exception):
    def __init__(self, message="Неправильный формат записи почты"):
        super().__init__(message) 

class YearValueError(Exception):
    def __init__(self, message="Значение не является годом"):
        super().__init__(message) 

class StockValueError(Exception):
    def __init__(self, message="Неправильный формат записи количества книг"):
        super().__init__(message) 

class PriceValueError(Exception):
    def __init__(self, message="Неправильный формат записи цены"):
        super().__init__(message) 

class BookNotFound(Exception):
    def __init__(self, message="Книга не найдена"):
        super().__init__(message) 

class OrderNotFound(Exception):
    def __init__(self, message="Заказ не найден"):
        super().__init__(message) 

class StatusValueError(Exception):
    def __init__(self, message="Неверный статус"):
        super().__init__(message) 