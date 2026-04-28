from typing import Any, cast

import pytest

from dynamic_array import DynamicArray


def test_constructor_creates_empty_array() -> None:
    array = DynamicArray()

    assert array.size() == 0
    assert array.to_list() == []


def test_constructor_accepts_custom_capacity_and_growth() -> None:
    array = DynamicArray(initial_capacity=3, growth_factor=1.5)

    assert array.size() == 0
    assert array.to_list() == []


@pytest.mark.parametrize("initial_capacity", [0, -1, -10])
def test_constructor_rejects_invalid_initial_capacity(
    initial_capacity: int,
) -> None:
    with pytest.raises(ValueError):
        DynamicArray(initial_capacity=initial_capacity)


@pytest.mark.parametrize("growth_factor", [1.0, 0.5, 0.0, -2.0])
def test_constructor_rejects_invalid_growth_factor(
    growth_factor: float,
) -> None:
    with pytest.raises(ValueError):
        DynamicArray(growth_factor=growth_factor)


def test_add_appends_values() -> None:
    array = DynamicArray()

    array.add("a")
    array.add("b")
    array.add("c")

    assert array.size() == 3
    assert array.to_list() == ["a", "b", "c"]


def test_add_resizes_when_capacity_is_full() -> None:
    array = DynamicArray(initial_capacity=1, growth_factor=2.0)

    array.add("a")
    array.add("b")
    array.add("c")

    assert array.size() == 3
    assert array.to_list() == ["a", "b", "c"]
    assert array._capacity >= array.size()


def test_get_returns_value_by_index() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    assert array.get(0) == "a"
    assert array.get(1) == "b"
    assert array.get(2) == "c"


def test_set_replaces_value_by_index() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    array.set(1, "x")

    assert array.to_list() == ["a", "x", "c"]


def test_remove_first_element() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(0)

    assert removed == "a"
    assert array.to_list() == ["b", "c"]
    assert array.size() == 2


def test_remove_middle_element() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(1)

    assert removed == "b"
    assert array.to_list() == ["a", "c"]
    assert array.size() == 2


def test_remove_last_element() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(2)

    assert removed == "c"
    assert array.to_list() == ["a", "b"]
    assert array.size() == 2


@pytest.mark.parametrize("index", [-1, 0])
def test_get_rejects_invalid_index_for_empty_array(index: int) -> None:
    array = DynamicArray()

    with pytest.raises(IndexError):
        array.get(index)


@pytest.mark.parametrize("index", [-1, 3])
def test_get_rejects_invalid_index(index: int) -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.get(index)


@pytest.mark.parametrize("index", [-1, 3])
def test_set_rejects_invalid_index(index: int) -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.set(index, "x")


@pytest.mark.parametrize("index", [-1, 3])
def test_remove_rejects_invalid_index(index: int) -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.remove(index)


def test_member_finds_existing_values() -> None:
    array = DynamicArray()
    array.from_list(["a", None, 42])

    assert array.member("a")
    assert array.member(None)
    assert array.member(42)


def test_member_returns_false_for_missing_values() -> None:
    array = DynamicArray()
    array.from_list(["a", "b"])

    assert not array.member("x")
    assert not array.member(None)


def test_reverse_empty_array() -> None:
    array = DynamicArray()

    array.reverse()

    assert array.to_list() == []


def test_reverse_multiple_values() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    array.reverse()

    assert array.to_list() == ["c", "b", "a"]


def test_from_list_replaces_existing_contents() -> None:
    array = DynamicArray()
    array.from_list(["old"])
    array.from_list(["new", "values"])

    assert array.to_list() == ["new", "values"]
    assert array.size() == 2


def test_to_list_returns_only_logical_values() -> None:
    array = DynamicArray(initial_capacity=5)
    array.add("a")
    array.add("b")

    assert array.to_list() == ["a", "b"]


def test_filter_modifies_array_in_place() -> None:
    array = DynamicArray()
    array.from_list([1, 2, 3, 4])

    array.filter(lambda value: isinstance(value, int) and value % 2 == 0)

    assert array.to_list() == [2, 4]
    assert array.size() == 2


def test_filter_can_remove_all_values() -> None:
    array = DynamicArray()
    array.from_list(["a", "b"])

    array.filter(lambda value: value is None)

    assert array.to_list() == []
    assert array.size() == 0


def test_map_modifies_array_in_place() -> None:
    array = DynamicArray()
    array.from_list([1, 2, 3])

    array.map(str)

    assert array.to_list() == ["1", "2", "3"]


def test_map_may_change_element_types() -> None:
    array = DynamicArray()
    array.from_list([1, None, "x"])

    array.map(lambda value: str(value))

    assert array.to_list() == ["1", "None", "x"]


def test_reduce_empty_array() -> None:
    array = DynamicArray()

    result = array.reduce(lambda state, value: state + 1, 0)

    assert result == 0


def test_reduce_multiple_values() -> None:
    array = DynamicArray()
    array.from_list([1, 2, 3])

    result = array.reduce(lambda state, value: state + value, 0)

    assert result == 6


def test_iterator_returns_values_in_order() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    result = []
    for value in array:
        result.append(value)

    assert result == ["a", "b", "c"]


def test_iterator_does_not_modify_array() -> None:
    array = DynamicArray()
    array.from_list(["a", "b", "c"])

    result = list(array)

    assert result == ["a", "b", "c"]
    assert array.to_list() == ["a", "b", "c"]
    assert array.size() == 3


def test_empty_creates_empty_array() -> None:
    array = DynamicArray.empty()

    assert isinstance(array, DynamicArray)
    assert array.size() == 0
    assert array.to_list() == []


def test_concat_appends_other_array_and_returns_self() -> None:
    left = DynamicArray()
    right = DynamicArray()
    left.from_list(["a", "b"])
    right.from_list(["c", "d"])

    result = left.concat(right)

    assert result is left
    assert left.to_list() == ["a", "b", "c", "d"]
    assert right.to_list() == ["c", "d"]


def test_concat_with_empty_right_array() -> None:
    left = DynamicArray()
    right = DynamicArray.empty()
    left.from_list(["a", "b"])

    left.concat(right)

    assert left.to_list() == ["a", "b"]
    assert right.to_list() == []


def test_concat_rejects_non_dynamic_array() -> None:
    array = DynamicArray()

    with pytest.raises(TypeError):
        array.concat(cast(Any, ["not", "a", "dynamic array"]))


def test_none_is_valid_user_value() -> None:
    array = DynamicArray()

    array.add(None)
    array.add("x")
    array.set(1, None)
    removed = array.remove(0)

    assert removed is None
    assert array.to_list() == [None]
    assert array.member(None)


def test_mixed_element_types_are_allowed() -> None:
    array = DynamicArray()
    array.from_list([1, "two", None, True])

    assert array.to_list() == [1, "two", None, True]
    assert array.get(0) == 1
    assert array.get(1) == "two"
    assert array.get(2) is None
    assert array.get(3) is True
