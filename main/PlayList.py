from main.Composition import Composition
from main.linked_list import LinkedList


class PlayList(LinkedList):
    def __init__(self):
        super().__init__(None)
        self.current_node = None

    def add_song(self, composition: Composition):
        self.append(composition)
        if self.current_node is None:
            self.current_node = self.first_item

    def remove_song(self, composition: Composition):
        self.remove(composition)
        if self.first_item is None:
            self.current_node = None
        elif self.current_node.data == composition:
            self.current_node = self.first_item

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

    def find_node(self, data):
        current = self.first_item
        while current is not None:
            if current.data == data:
                return current
            current = current.next_item
        return None

    def get_all_songs(self):
        return [node.data for node in self]