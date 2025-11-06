class LinkedListItem:
    """
    Узел двусвязного списка.

    Attributes:
        data: Данные, хранимые в узле.
        _next_item (LinkedListItem | None): Ссылка на следующий узел.
        _previous_item (LinkedListItem | None): Ссылка на предыдущий узел.
    """
    def __init__(self, data=None):
        """
        Инициализация узла списка.

        Args:
            data: Данные для хранения в узле (по умолчанию None).
        """
        self.data = data
        self._next_item = None
        self._previous_item = None

    @property
    def next_item(self):
        """Возвращает следующий элемент списка (LinkedListItem или None)."""
        return self._next_item

    @next_item.setter
    def next_item(self, node):
        """
        Устанавливает следующий элемент с защитой от бесконечной рекурсии.

        Args:
            node (LinkedListItem | None): Узел, который станет следующим.
        """
        self._next_item = node
        # защита от бесконечной рекурсии
        if node is not None and node._previous_item is not self:
            node._previous_item = self

    @property
    def previous_item(self):
        """Возвращает предыдущий элемент списка (LinkedListItem или None)."""
        return self._previous_item

    @previous_item.setter
    def previous_item(self, node):
        """
        Устанавливает предыдущий элемент с защитой от бесконечной рекурсии.

        Args:
            node (LinkedListItem | None): Узел, который станет предыдущим.
        """
        self._previous_item = node
        if node is not None and node._next_item is not self:
            node._next_item = self

    def __repr__(self):
        """Строковое представление узла для отладки."""
        return f"Node (data={self.data}, _next_item={self._next_item}, _previous_item={self._previous_item})"


class LinkedList:
    """
    Кольцевой двусвязный список.

    Attributes:
        _head (LinkedListItem | None): Первый элемент списка.
    """
    def __init__(self, first_item=None):
        """
        Инициализация списка.

        Args:
            first_item (LinkedListItem | None): Первый узел списка (по умолчанию None).
        """
        self._head = first_item

    @property
    def first_item(self):
        """Возвращает первый элемент списка (LinkedListItem или None)."""
        return self._head

    @property
    def last(self):
        """Возвращает последний элемент списка (LinkedListItem или None)."""
        if not self.first_item:
            return None
        return self._head.previous_item

    def append_left(self, item):
        """
        Добавляет элемент в начало списка.

        Args:
            item: Данные для нового узла.
        """
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
        """
        Добавляет элемент в конец списка.

        Args:
            item: Данные для нового узла.
        """
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
        """Синоним метода append_right."""
        self.append_right(item)

    def remove(self, item):
        """
        Удаляет первый найденный элемент из списка.

        Args:
            item: Данные для удаления.

        Raises:
            ValueError: Если список пуст или элемент не найден.
        """
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
        """
        Вставляет новый элемент справа от указанного элемента.

        Args:
            previous: Данные узла, после которого вставляем.
            item: Данные для нового узла.

        Raises:
            ValueError: Если список пуст или предыдущий узел не найден.
        """
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
        """Возвращает количество элементов в списке."""
        if self.first_item is None:
            return 0
        count = 1
        current = self._head.next_item
        while current and current is not self._head:
            count += 1
            current = current.next_item
        return count

    def __iter__(self):
        """Итератор по узлам списка (LinkedListItem)."""
        if not self.first_item:
            return
        current = self._head
        yield current
        current = current.next_item
        while current is not self._head:
            yield current
            current = current.next_item

    def __getitem__(self, index):
        """
        Доступ к элементу по индексу.

        Args:
            index (int): Индекс элемента (может быть отрицательным).

        Returns:
            Любые данные, хранящиеся в узле.

        Raises:
            IndexError: Если индекс вне диапазона.
        """
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
        """
        Проверяет наличие элемента в списке.

        Args:
            item: Данные для поиска.

        Returns:
            bool: True, если элемент найден, иначе False.
        """
        for node in self:
            if node.data == item:
                return True
        return False

    def __reversed__(self):
        """Итератор по элементам списка в обратном порядке."""
        if not self.first_item:
            return
        current = self.last
        yield current.data
        current = current.previous_item
        while current is not self.last:
            yield current.data
            current = current.previous_item