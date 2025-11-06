class LinkedListItem:
    """Узел двусвязного списка"""
    def __init__(self, data=None):
        self.data = data
        self._next_item = None
        self._previous_item = None
        #print(repr(self))

    @property
    def next_item(self):
        """Следующий элемент"""
        return self._next_item

    @next_item.setter
    def next_item(self, node):
        """Сеттер next_item с защитой от бесконечной рекурсии"""
        self._next_item = node
        # защита от бесконечной рекурсии
        if node is not None and node._previous_item is not self:
            node._previous_item = self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        return self._previous_item

    @previous_item.setter
    def previous_item(self, node):
        """Сеттер previous_item с защитой от бесконечной рекурсии"""
        self._previous_item = node
        if node is not None and node._next_item is not self:
            node._next_item = self

    def __repr__(self):
        return f"Node (data={self.data}, _next_item={self._next_item}, _previous_item={self._previous_item})"


class LinkedList:
    """Кольцевой двусвязанный список"""
    def __init__(self, first_item=None):
        self._head = first_item

    @property
    def first_item(self):
        return self._head

    @property
    def last(self):
        """Последний элемент"""
        if not self.first_item:
            return None
        return self._head.previous_item

    def append_left(self, item):
        """Добавление слева"""
        new_node = LinkedListItem(item)
        if not self._head:
            new_node.next_item = new_node
            new_node.previous_item = new_node
            self._head = new_node
            return
        last = self.last
        new_node.next_item = self._head
        new_node.previous_item = last
        last.next_item = new_node
        self._head.previous_item = new_node
        self._head = new_node


    def append_right(self, item):
        """Добавление справа"""
        if not self._head:
            self.append_left(item)
        else:
            last = self.last
            new_node = LinkedListItem(item)
            new_node.next_item = self._head
            new_node.previous_item = last
            last.next_item = new_node
            self._head.previous_item = new_node

    def append(self, item):
        """Синоним append_right"""
        self.append_right(item)

    def remove(self, item):
        """Удаление"""
        if not self.first_item:
            raise ValueError("list is empty")
        current = self.first_item
        while True:
            if current.data == item:
                if current.next_item is current: #Ищем первое вхождение
                    self._head = None
                    return
                current.previous_item.next_item = current.next_item
                current.next_item.previous_item = current.previous_item
                if current is self._head:
                    self._head = current.next_item
                return
            current = current.next_item
            if current is self._head:
                break
        raise ValueError("item not found")

    def insert(self, previous, item):
        """Вставка справа"""
        if not self.first_item:
            raise ValueError("list is empty")
        current = self.first_item
        while True:
            if current.data == previous:
                new_node = LinkedListItem(item)
                next_node = current.next_item
                current.next_item = new_node
                new_node.previous_item = current
                new_node.next_item = next_node
                next_node.previous_item = new_node
                return
            current = current.next_item
            if current is self.first_item:
                break
        raise ValueError("node not found")


    def __len__(self):
        """Магический метод выдающий размер списка"""
        if self.first_item is None:
            return 0
        count = 1
        current = self._head.next_item
        while current and current is not self._head:
            count += 1
            current = current.next_item
        return count

    def __iter__(self):
        if not self.first_item:
            return
        current = self._head
        yield current
        current = current.next_item
        while current is not self._head:
            yield current
            current = current.next_item

    def __getitem__(self, index):
        """Доступ по индексу"""
        size = len(self)
        if index < 0:
            index += size
        if index < 0 or index >= size:
            raise IndexError("index out of range")
        current = self._head
        for _ in range(index):
            current = current.next_item
        return current.data

    def __contains__(self, item):
        """Поддержка оператора in"""
        for node in self:
            if node.data == item:
                return True
        return False

    def __reversed__(self):
        if not self.first_item:
            return
        current = self.last
        yield current.data
        current = current.previous_item
        while current is not self.last:
            yield current.data
            current = current.previous_item