from __future__ import annotations

from typing import Any, Callable, Generator, Generic, Iterable, TypeVar, cast

T = TypeVar("T")
S = TypeVar("S")

_EMPTY = object()


class DynamicArray(Generic[T]):
    """A mutable dynamic array with manual capacity management."""

    def __init__(
        self,
        initial_capacity: int = 1,
        growth_factor: float = 2.0,
    ) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be at least 1")
        if growth_factor <= 1:
            raise ValueError("growth_factor must be greater than 1")

        self._capacity = initial_capacity
        self._growth_factor = growth_factor
        self._length = 0
        self._data: list[object] = [_EMPTY] * self._capacity

    def __eq__(self, other: object) -> bool:
        """Compare arrays by logical contents, not by internal capacity."""
        if not isinstance(other, DynamicArray):
            return False
        return self.to_list() == other.to_list()

    def add(self, value: T) -> None:
        if self._length == self._capacity:
            self._resize()

        self._data[self._length] = value
        self._length += 1

    def get(self, index: int) -> T:
        self._check_index(index)
        return self._value_at(index)

    def set(self, index: int, value: T) -> None:
        self._check_index(index)
        self._data[index] = value

    def remove(self, index: int) -> T:
        self._check_index(index)
        removed = self._value_at(index)

        for current in range(index, self._length - 1):
            self._data[current] = self._data[current + 1]

        self._length -= 1
        self._data[self._length] = _EMPTY
        return removed

    def size(self) -> int:
        return self._length

    def member(self, value: object) -> bool:
        for index in range(self._length):
            if self._value_at(index) == value:
                return True
        return False

    def reverse(self) -> None:
        left = 0
        right = self._length - 1

        while left < right:
            self._data[left], self._data[right] = (
                self._data[right],
                self._data[left],
            )
            left += 1
            right -= 1

    def from_list(self, values: Iterable[T]) -> None:
        items = list(values)
        self._capacity = max(1, len(items))
        self._data = [_EMPTY] * self._capacity
        self._length = len(items)

        for index, value in enumerate(items):
            self._data[index] = value

    def to_list(self) -> list[T]:
        return [self._value_at(index) for index in range(self._length)]

    def filter(self, predicate: Callable[[T], bool]) -> None:
        write_index = 0

        for read_index in range(self._length):
            value = self._value_at(read_index)
            if predicate(value):
                self._data[write_index] = value
                write_index += 1

        for index in range(write_index, self._length):
            self._data[index] = _EMPTY

        self._length = write_index

    def map(self, function: Callable[[T], Any]) -> None:
        for index in range(self._length):
            self._data[index] = function(self._value_at(index))

    def reduce(
        self,
        function: Callable[[S, T], S],
        initial_state: S,
    ) -> S:
        state = initial_state

        for index in range(self._length):
            state = function(state, self._value_at(index))

        return state

    def values(self) -> Generator[T, None, None]:
        """Generate logical array values in order.

        Empty internal slots are not exposed.
        """
        for index in range(self._length):
            yield self._value_at(index)

    def __iter__(self) -> Generator[T, None, None]:
        return self.values()

    @classmethod
    def empty(cls) -> DynamicArray[T]:
        return cls()

    def concat(self, other: DynamicArray[T]) -> DynamicArray[T]:
        if not isinstance(other, DynamicArray):
            raise TypeError("other must be a DynamicArray")

        for value in other:
            self.add(value)

        return self

    def _resize(self) -> None:
        new_capacity = int(self._capacity * self._growth_factor)
        new_capacity = max(self._capacity + 1, new_capacity)
        new_data: list[object] = [_EMPTY] * new_capacity

        for index in range(self._length):
            new_data[index] = self._data[index]

        self._data = new_data
        self._capacity = new_capacity

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self._length:
            raise IndexError("index out of range")

    def _value_at(self, index: int) -> T:
        return cast(T, self._data[index])
