from typing import Any, Callable, Iterator


class DynamicArray:
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
        self._data: list[object] = [None] * self._capacity

    def add(self, value: object) -> None:
        if self._length == self._capacity:
            self._resize()

        self._data[self._length] = value
        self._length += 1

    def get(self, index: int) -> object:
        self._check_index(index)
        return self._data[index]

    def set(self, index: int, value: object) -> None:
        self._check_index(index)
        self._data[index] = value

    def remove(self, index: int) -> object:
        self._check_index(index)
        removed = self._data[index]

        for current in range(index, self._length - 1):
            self._data[current] = self._data[current + 1]

        self._length -= 1
        self._data[self._length] = None
        return removed

    def size(self) -> int:
        return self._length

    def member(self, value: object) -> bool:
        for index in range(self._length):
            if self._data[index] == value:
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

    def from_list(self, values: list[object]) -> None:
        self._capacity = max(1, len(values))
        self._data = [None] * self._capacity
        self._length = len(values)

        for index, value in enumerate(values):
            self._data[index] = value

    def to_list(self) -> list[object]:
        return [self._data[index] for index in range(self._length)]

    def filter(self, predicate: Callable[[object], bool]) -> None:
        write_index = 0

        for read_index in range(self._length):
            value = self._data[read_index]
            if predicate(value):
                self._data[write_index] = value
                write_index += 1

        for index in range(write_index, self._length):
            self._data[index] = None

        self._length = write_index

    def map(self, function: Callable[[object], object]) -> None:
        for index in range(self._length):
            self._data[index] = function(self._data[index])

    def reduce(
        self,
        function: Callable[[Any, object], Any],
        initial_state: Any,
    ) -> Any:
        state = initial_state

        for index in range(self._length):
            state = function(state, self._data[index])

        return state

    def __iter__(self) -> Iterator[object]:
        for index in range(self._length):
            yield self._data[index]

    @classmethod
    def empty(cls) -> "DynamicArray":
        return cls()

    def concat(self, other: "DynamicArray") -> "DynamicArray":
        if not isinstance(other, DynamicArray):
            raise TypeError("other must be a DynamicArray")

        for value in other:
            self.add(value)

        return self

    def _resize(self) -> None:
        new_capacity = int(self._capacity * self._growth_factor)
        new_capacity = max(self._capacity + 1, new_capacity)

        new_data: list[object] = [None] * new_capacity

        for index in range(self._length):
            new_data[index] = self._data[index]

        self._data = new_data
        self._capacity = new_capacity

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self._length:
            raise IndexError("index out of range")
