class FormatFileError(Exception):
    def __init__(self, message="Расширение файла должно быть json или xml"):
        super().__init__(message)
