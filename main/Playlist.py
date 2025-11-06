from .composition import Composition
from .linked_list import LinkedList


class PlayList(LinkedList):
    """
    Плейлист — кольцевой двусвязный список музыкальных композиций.

    Наследует LinkedList и добавляет логику управления текущей композицией.

    Attributes:
        current_node (LinkedListItem | None): Узел текущей композиции.
    """
    def __init__(self):
        """
        Инициализация пустого плейлиста.
        """
        super().__init__(None)
        self.current_node = None

    def add_song(self, composition: Composition):
        """
        Добавляет композицию в плейлист.

        Если плейлист был пустым, текущей композицией становится добавленный трек.

        Args:
            composition (Composition): Объект композиции для добавления.
        """
        self.append(composition)
        if self.current_node is None:
            self.current_node = self.first_item

    def remove_song(self, composition: Composition):
        """
        Удаляет композицию из плейлиста.

        Обновляет current_node, если он указывает на удаляемый узел.

        Args:
            composition (Composition): Объект композиции для удаления.
        """
        node_to_remove = self.find_node(composition)

        if not node_to_remove:
            return  # композиция не найдена

        # Обновляем current_node, если он указывает на удаляемый узел
        if self.current_node == node_to_remove:

            if node_to_remove.next_item and node_to_remove.next_item != node_to_remove:
                self.current_node = node_to_remove.next_item
            elif node_to_remove.previous_item and node_to_remove.previous_item != node_to_remove:
                self.current_node = node_to_remove.previous_item
            else:
                self.current_node = None

        # Вызов твоей функции remove, которая обновляет связи и _head
        self.remove(composition)

    def next_song(self):
        """
        Переключает на следующий трек в плейлисте.

        Returns:
            Composition | None: Следующая композиция или None, если плейлист пуст.
        """
        if self.current_node:
            self.current_node = self.current_node.next_item
            return self.current_node.data
        return None

    def previous_song(self):
        """
        Переключает на предыдущий трек в плейлисте.

        Returns:
            Composition | None: Предыдущая композиция или None, если плейлист пуст.
        """
        if self.current_node:
            self.current_node = self.current_node.previous_item
            return self.current_node.data
        return None

    def get_current(self):
        """
        Возвращает текущую композицию плейлиста.

        Returns:
            Composition | None: Текущая композиция или None, если плейлист пуст.
        """
        if self.current_node:
            return self.current_node.data
        return None

    def move_up(self, composition: Composition):
        """
        Перемещает композицию на одну позицию вверх в плейлисте.

        Обменивает данные узлов, не изменяя ссылки.

        Args:
            composition (Composition): Объект композиции для перемещения.
        """
        node = self.find_node(composition)
        if node and node.previous_item:
            prev_node = node.previous_item
            # меняем местами данные
            node.data, prev_node.data = prev_node.data, node.data
            if self.current_node == node:
                self.current_node = node

    def move_down(self, composition: Composition):
        """
        Перемещает композицию на одну позицию вниз в плейлисте.

        Обменивает данные узлов, не изменяя ссылки.

        Args:
            composition (Composition): Объект композиции для перемещения.
        """
        node = self.find_node(composition)
        if node and node.next_item:
            next_node = node.next_item
            # меняем местами данные
            node.data, next_node.data = next_node.data, node.data
            if self.current_node == node:
                self.current_node = node

    def find_node(self, data):
        """
        Ищет узел по данным.

        Args:
            data (Composition): Данные для поиска.

        Returns:
            LinkedListItem | None: Узел с соответствующими данными или None, если не найден.
        """
        current = self.first_item
        if not current:
            return None
        while True:
            if current.data == data:
                return current
            current = current.next_item
            if current == self.first_item:
                print(3)
                break
        return None

    def get_all_songs(self):
        """
        Возвращает все композиции в плейлисте.

        Returns:
            list[Composition]: Список всех композиций.
        """
        return [node.data for node in self]