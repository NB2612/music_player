from .Composition import Composition
from .linked_list import LinkedList


class PlayList(LinkedList):
    def __init__(self):
        super().__init__(None)
        self.current_node = None

    def add_song(self, composition: Composition):
        """Добавление песни в плейлист"""
        self.append(composition)
        if self.current_node is None:
            self.current_node = self.first_item

    def remove_song(self, composition: Composition):
        """Удаление композиции из плейлиста с использованием базового remove"""
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
        if self.current_node:
            self.current_node = self.current_node.next_item
            return self.current_node.data
        return None

    def previous_song(self):
        if self.current_node:
            self.current_node = self.current_node.previous_item
            return self.current_node.data
        return None

    def get_current(self):
        if self.current_node:
            return self.current_node.data
        return None

    def move_up(self, composition: Composition):
        """Перемещает композицию на одну позицию вверх"""
        node = self.find_node(composition)
        if node and node.previous_item:
            prev_node = node.previous_item
            # меняем местами данные
            node.data, prev_node.data = prev_node.data, node.data
            if self.current_node == node:
                self.current_node = node

    def move_down(self, composition: Composition):
        """Перемещает композицию на одну позицию вниз"""
        node = self.find_node(composition)
        if node and node.next_item:
            next_node = node.next_item
            # меняем местами данные
            node.data, next_node.data = next_node.data, node.data
            if self.current_node == node:
                self.current_node = node

    def find_node(self, data):
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
        return [node.data for node in self]