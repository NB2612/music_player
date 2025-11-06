import pathlib


class Composition:
    """Представляет музыкальную композицию."""
    def __init__(self, title: str, duration: float, path: str):
        """Представляет музыкальную композицию.
        Args: title(str) - название трека
        duration(int) - продолжительность в секундах
        path(str) - путь к треку"""
        self.title = title
        self.duration = duration
        self.path = path
        #print(repr(self))

    def get_path(self):
        return str(self.path)

    def get_title(self):
        return str(self.title)

    def get_duration(self):
        return float(self.duration)

    def __repr__(self):
        """Возвращает строковое представление для отладки."""
        return f"Composition('{self.title}', '{self.duration}', '{self.path}')"

    def __eq__(self, other):
        """Поддержка оператора == для сравнения композиций."""
        if isinstance(other, Composition):
            return (self.title, self.duration, self.path) == \
                (other.title, other.duration, other.path)
        if isinstance(other, str):
            return self.title == other or self.path == other
        if isinstance(other, float):
            return self.duration == other
        return False
