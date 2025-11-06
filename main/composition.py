class Composition:
    """
    Представляет музыкальную композицию.

    Attributes:
        title (str): Название трека.
        duration (float): Продолжительность трека в секундах.
        path (str): Путь к аудиофайлу.
    """
    def __init__(self, title: str, duration: float, path: str):
        """
        Инициализация объекта Composition.

        Args:
            title (str): Название трека.
            duration (float): Продолжительность трека в секундах.
            path (str): Путь к аудиофайлу.
        """
        self.title = title
        self.duration = duration
        self.path = path
        #print(repr(self))

    def get_path(self):
        """
        Возвращает путь к файлу композиции.

        Returns:
            str: Путь к аудиофайлу.
        """
        return str(self.path)

    def get_title(self):
        """
        Возвращает название композиции.

        Returns:
            str: Название трека.
        """
        return str(self.title)

    def get_duration(self):
        """
        Возвращает длительность композиции в секундах.

        Returns:
            float: Длительность трека.
        """
        return float(self.duration)

    def __repr__(self):
        """
        Возвращает строковое представление объекта для отладки.

        Returns:
            str: Строка в формате "Composition('title', 'duration', 'path')".
        """
        return f"Composition('{self.title}', '{self.duration}', '{self.path}')"

    def __eq__(self, other):
        """
        Сравнивает текущую композицию с другой.

        Сравнение поддерживает:
        - Другая Composition: сравнение title, duration и path.
        - Строка: совпадение с title или path.
        - Число (int или float): сравнение с duration.

        Args:
            other (Composition | str | int | float): Объект для сравнения.

        Returns:
            bool: True, если объекты равны по соответствующему критерию, иначе False.
        """
        if isinstance(other, Composition):
            return (self.title, self.duration, self.path) == (other.title, other.duration, other.path)

        if isinstance(other, str):
            return self.title == other or self.path == other

        if isinstance(other, (int, float)):
            return self.duration == other

        return False
