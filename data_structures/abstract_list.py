from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.dunder_protected import DunderProtected

T = TypeVar('T')


class List(ABC, Generic[T], DunderProtected):
    """ List ADT. 
    Defines a generic abstract list with the standard methods.
    """
    @abstractmethod
    def insert(self, index: int, item: T) -> None:
        """ Insert an item at the given position. """
        pass

    def append(self, item: T) -> None:
        """ Append a new item to the end of the list. """
        self.insert(len(self), item)

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        pass

    def remove(self, item: T) -> None:
        """ Remove an item from the list. """
        index = self.index(item)
        self.delete_at_index(index)

    @abstractmethod
    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        pass

    def is_empty(self) -> bool:
        """ Check if the list of empty. """
        return len(self) == 0

    @abstractmethod
    def clear(self) -> None:
        """ Clear the list. """
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """ Return the element at the given position. """
        pass

    @abstractmethod
    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at the given position. """
        pass

    def __contains__(self, item: T) -> bool:
        """ Checks if the item is in the list. """
        try:
            _ = self.index(item)
            return True
        except ValueError:
            return False

    @abstractmethod
    def __len__(self) -> int:
        """ Return the length of the list. """
        pass

    def __str__(self) -> str:
        """ String representation of the list object. """
        strings = (str(item) for item in (self))

        return '[' + ', '.join(strings) + ']'

    def __repr__(self) -> str:
        return str(self)
