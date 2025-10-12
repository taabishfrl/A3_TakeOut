from data_structures.abstract_list import List, T
from data_structures.node import Node


class LinkedListIterator:
    """ Iterator for LinkedList. """
    def __init__(self, head_node: Node):
        self.__current = head_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current is None:
            raise StopIteration
        else:
            item = self.__current.item
            self.__current = self.__current.link
            return item


class LinkedList(List[T]):
    """ Linked-node based implementation of List ADT. """

    def __init__(self):
        self.__head = None
        self.__rear = None
        self.__length = 0

    def insert(self, index: int, item: T) -> None:
        """
        Inserts a new item before position index.
        :Complexity Analysis:
            ...t: O(1) if adding to the beginning or end of the list.
            Worst: O(N) where N is the number of items in the list. Occurs when inserting towards the end of the list (but not at the end).
        """
        if index == len(self):
            self.append(item)
        else:
            new_node = Node(item)
            if index == 0:
                new_node.link = self.__head
                self.__head = new_node
            else:
                previous_node = self.__get_node_at_index(index-1)
                new_node.link = previous_node.link
                previous_node.link = new_node

            self.__length += 1

    def append(self, item: T) -> None:
        """ Append the item to the end of the list.
        :complexity: Given we have a reference to the rear of the list, this is O(1).
        """
        new_node = Node(item)
        if self.__head is None:
            self.__head = new_node
        else:
            self.__rear.link = new_node
        self.__rear = new_node
        self.__length += 1

    def clear(self):
        """ Clear the list. """
        List.clear(self)
        self.__head = None
        self.__rear = None
        self.__length = 0

    def delete_at_index(self, index: int) -> T:
        """
        Deletes an item at position index.
        :Complexity Analysis:
            ...t: O(1) Deleting the first item in the list.
            Worst: O(N) Deleting the last item in the list, where N is the number of items in the list.
        """
        if not self.is_empty():
            if index > 0:
                previous_node = self.__get_node_at_index(index-1)
                item = previous_node.link.item
                previous_node.link = previous_node.link.link
            elif index == 0:
                item = self.__head.item
                self.__head = self.__head.link
                previous_node = self.__head
            else:
                raise ValueError("Index out of bounds")

            if index == len(self) - 1:
                self.__rear = previous_node

            self.__length -= 1
            return item
        else:
            raise ValueError("Index out of bounds: list is empty")

    def index(self, item: T) -> int:
        """
        Find the position of a given item in the list.
        :Complexity Analysis:
            ...t: O(1) if the item is at the head of the list.
            Worst: O(N) where N is the number of items in the list. Happens when the item is at
                the end of the list or it doesn't exist in the list.
        """
        current = self.__head
        index = 0
        while current is not None and current.item != item:
            current = current.link
            index += 1
        if current is None:
            raise ValueError('Item is not in list')
        else:
            return index

    def __get_node_at_index(self, index: int) -> Node[T]:
        """
        Gets the nodes at a given index
        :Complexity Analysis:
            ...t: O(1) if the index is 0 or len(list) - 1
            Worst: O(N) where N is the number of items in the list. Happens when the item is close
                to the end of the list or it doesn't exist in the list.
        """
        if -1 * len(self) <= index and index < len(self):
            if index < 0:
                index = len(self) + index
            elif index == len(self) - 1:
                return self.__rear
            current = self.__head
            for _ in range(index):
                current = current.link
            return current
        else:
            raise IndexError('Out of bounds access in list.')

    def __getitem__(self, index: int) -> T:
        """ Return the element at a given position.
        :complexity: See self.__get_node_at_index().
        """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at a given position.
        :complexity: See self.__get_node_at_index().
        """
        node_at_index = self.__get_node_at_index(index)
        node_at_index.item = item

    def __iter__(self):
        """ Iterate through the list. """
        return LinkedListIterator(self.__head)

    def __len__(self) -> int:
        """ Return the length of the list. """
        return self.__length

    def __str__(self) -> str:
        if not len(self):
            return "<LinkedList []>"

        return "<LinkedList [" + ", ".join(str(item) for item in self) + "]>"
