from __future__ import annotations

from typing import Any, cast

import hypothesis.strategies as st
import pytest
from hypothesis import given
from hypothesis.strategies import SearchStrategy

from dynamic_array import DynamicArray


MIXED_VALUES: SearchStrategy[Any] = st.one_of(
    st.none(),
    st.integers(min_value=-1000, max_value=1000),
    st.text(max_size=20),
    st.booleans(),
)
MIXED_LISTS: SearchStrategy[list[Any]] = st.lists(MIXED_VALUES, max_size=30)
GROWTH_FACTORS: SearchStrategy[float] = st.floats(
    min_value=1.1,
    max_value=4.0,
    allow_nan=False,
    allow_infinity=False,
)
CAPACITIES: SearchStrategy[int] = st.integers(min_value=1, max_value=10)


def make_array(values: list[Any]) -> DynamicArray[Any]:
    array: DynamicArray[Any] = DynamicArray()
    array.from_list(values)
    return array


def make_array_with_config(
    values: list[Any],
    initial_capacity: int,
    growth_factor: float,
) -> DynamicArray[Any]:
    array: DynamicArray[Any] = DynamicArray(
        initial_capacity=initial_capacity,
        growth_factor=growth_factor,
    )
    for value in values:
        array.add(value)
    return array


def make_array_and_values(
    values: list[Any],
    initial_capacity: int,
    growth_factor: float,
) -> tuple[DynamicArray[Any], list[Any]]:
    array = make_array_with_config(
        values,
        initial_capacity,
        growth_factor,
    )
    return array, values


def dynamic_array_strategy() -> SearchStrategy[DynamicArray[Any]]:
    return st.builds(
        make_array_with_config,
        MIXED_LISTS,
        CAPACITIES,
        GROWTH_FACTORS,
    )


def dynamic_array_and_values_strategy() -> SearchStrategy[
    tuple[DynamicArray[Any], list[Any]]
]:
    return st.builds(
        make_array_and_values,
        MIXED_LISTS,
        CAPACITIES,
        GROWTH_FACTORS,
    )


def test_constructor_creates_empty_array() -> None:
    array: DynamicArray[Any] = DynamicArray()

    assert array.size() == 0
    assert array.to_list() == []


def test_constructor_accepts_custom_capacity_and_growth() -> None:
    array: DynamicArray[Any] = DynamicArray(
        initial_capacity=3,
        growth_factor=1.5,
    )

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
    array: DynamicArray[str] = DynamicArray()

    array.add("a")
    array.add("b")
    array.add("c")

    assert array.size() == 3
    assert array.to_list() == ["a", "b", "c"]


def test_add_resizes_when_capacity_is_full() -> None:
    array: DynamicArray[str] = DynamicArray(
        initial_capacity=1,
        growth_factor=2.0,
    )

    array.add("a")
    array.add("b")
    array.add("c")

    assert array.size() == 3
    assert array.to_list() == ["a", "b", "c"]
    assert array._capacity >= array.size()


def test_get_returns_value_by_index() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    assert array.get(0) == "a"
    assert array.get(1) == "b"
    assert array.get(2) == "c"


def test_set_replaces_value_by_index() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    array.set(1, "x")

    assert array.to_list() == ["a", "x", "c"]


def test_remove_first_element() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(0)

    assert removed == "a"
    assert array.to_list() == ["b", "c"]
    assert array.size() == 2


def test_remove_middle_element() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(1)

    assert removed == "b"
    assert array.to_list() == ["a", "c"]
    assert array.size() == 2


def test_remove_last_element() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    removed = array.remove(2)

    assert removed == "c"
    assert array.to_list() == ["a", "b"]
    assert array.size() == 2


@pytest.mark.parametrize("index", [-1, 0])
def test_get_rejects_invalid_index_for_empty_array(index: int) -> None:
    array: DynamicArray[Any] = DynamicArray()

    with pytest.raises(IndexError):
        array.get(index)


@pytest.mark.parametrize("index", [-1, 3])
def test_get_rejects_invalid_index(index: int) -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.get(index)


@pytest.mark.parametrize("index", [-1, 3])
def test_set_rejects_invalid_index(index: int) -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.set(index, "x")


@pytest.mark.parametrize("index", [-1, 3])
def test_remove_rejects_invalid_index(index: int) -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    with pytest.raises(IndexError):
        array.remove(index)


def test_member_finds_existing_values() -> None:
    array: DynamicArray[Any] = DynamicArray()
    array.from_list(["a", None, 42])

    assert array.member("a")
    assert array.member(None)
    assert array.member(42)


def test_member_returns_false_for_missing_values() -> None:
    array: DynamicArray[Any] = DynamicArray()
    array.from_list(["a", "b"])

    assert not array.member("x")
    assert not array.member(None)


def test_reverse_empty_array() -> None:
    array: DynamicArray[Any] = DynamicArray()

    array.reverse()

    assert array.to_list() == []


def test_reverse_multiple_values() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    array.reverse()

    assert array.to_list() == ["c", "b", "a"]


def test_from_list_replaces_existing_contents() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["old"])
    array.from_list(["new", "values"])

    assert array.to_list() == ["new", "values"]
    assert array.size() == 2


def test_from_list_accepts_iterables() -> None:
    array: DynamicArray[int] = DynamicArray()

    array.from_list(value for value in range(3))

    assert array.to_list() == [0, 1, 2]


def test_to_list_returns_only_logical_values() -> None:
    array: DynamicArray[str] = DynamicArray(initial_capacity=5)
    array.add("a")
    array.add("b")

    assert array.to_list() == ["a", "b"]


def test_filter_modifies_array_in_place() -> None:
    array: DynamicArray[int] = DynamicArray()
    array.from_list([1, 2, 3, 4])

    array.filter(lambda value: value % 2 == 0)

    assert array.to_list() == [2, 4]
    assert array.size() == 2


def test_filter_can_remove_all_values() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b"])

    array.filter(lambda value: value == "missing")

    assert array.to_list() == []
    assert array.size() == 0


def test_map_modifies_array_in_place() -> None:
    array: DynamicArray[int] = DynamicArray()
    array.from_list([1, 2, 3])

    array.map(lambda value: value + 1)

    assert array.to_list() == [2, 3, 4]


def test_map_may_change_element_types() -> None:
    array: DynamicArray[Any] = DynamicArray()
    array.from_list([1, None, "x"])

    array.map(str)

    assert array.to_list() == ["1", "None", "x"]


def test_reduce_empty_array() -> None:
    array: DynamicArray[int] = DynamicArray()

    result = array.reduce(lambda state, value: state + value, 0)

    assert result == 0


def test_reduce_multiple_values() -> None:
    array: DynamicArray[int] = DynamicArray()
    array.from_list([1, 2, 3])

    result = array.reduce(lambda state, value: state + value, 0)

    assert result == 6


def test_values_generator_returns_values_in_order() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    generator = array.values()

    assert iter(generator) is generator
    assert list(generator) == ["a", "b", "c"]
    assert array.to_list() == ["a", "b", "c"]


def test_iterator_returns_values_in_order() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    result = []
    for value in array:
        result.append(value)

    assert result == ["a", "b", "c"]


def test_iterator_does_not_modify_array() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a", "b", "c"])

    result = list(array)

    assert result == ["a", "b", "c"]
    assert array.to_list() == ["a", "b", "c"]
    assert array.size() == 3


def test_empty_creates_empty_array() -> None:
    array: DynamicArray[Any] = DynamicArray.empty()

    assert isinstance(array, DynamicArray)
    assert array.size() == 0
    assert array.to_list() == []


def test_concat_appends_other_array_and_returns_self() -> None:
    left: DynamicArray[str] = DynamicArray()
    right: DynamicArray[str] = DynamicArray()
    left.from_list(["a", "b"])
    right.from_list(["c", "d"])

    result = left.concat(right)

    assert result is left
    assert left.to_list() == ["a", "b", "c", "d"]
    assert right.to_list() == ["c", "d"]


def test_concat_with_empty_right_array() -> None:
    left: DynamicArray[str] = DynamicArray()
    right: DynamicArray[str] = DynamicArray.empty()
    left.from_list(["a", "b"])

    left.concat(right)

    assert left.to_list() == ["a", "b"]
    assert right.to_list() == []


def test_concat_rejects_non_dynamic_array() -> None:
    array: DynamicArray[Any] = DynamicArray()

    with pytest.raises(TypeError):
        array.concat(cast(Any, ["not", "a", "dynamic array"]))


def test_eq_compares_logical_values() -> None:
    left: DynamicArray[str] = DynamicArray(initial_capacity=1)
    right: DynamicArray[str] = DynamicArray(initial_capacity=10)
    left.from_list(["a", "b"])
    right.from_list(["a", "b"])

    assert left == right


def test_eq_detects_different_values() -> None:
    left: DynamicArray[str] = DynamicArray()
    right: DynamicArray[str] = DynamicArray()
    left.from_list(["a", "b"])
    right.from_list(["a", "c"])

    assert left != right


def test_eq_returns_false_for_other_types() -> None:
    array: DynamicArray[str] = DynamicArray()
    array.from_list(["a"])

    assert array != ["a"]


def test_none_is_valid_user_value() -> None:
    array: DynamicArray[Any] = DynamicArray()

    array.add(None)
    array.add("x")
    array.set(1, None)
    removed = array.remove(0)

    assert removed is None
    assert array.to_list() == [None]
    assert array.member(None)


def test_mixed_element_types_are_allowed() -> None:
    array: DynamicArray[Any] = DynamicArray()
    array.from_list([1, "two", None, True])

    assert array.to_list() == [1, "two", None, True]
    assert array.get(0) == 1
    assert array.get(1) == "two"
    assert array.get(2) is None
    assert array.get(3) is True


@given(dynamic_array_and_values_strategy())
def test_pbt_generated_array_matches_values(
    pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    array, values = pair

    assert array.to_list() == values
    assert array.size() == len(values)


@given(MIXED_LISTS)
def test_pbt_from_list_to_list_equality(values: list[Any]) -> None:
    array = make_array(values)

    assert array.to_list() == values


@given(dynamic_array_and_values_strategy())
def test_pbt_size_equals_python_list_length(
    pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    array, values = pair

    assert array.size() == len(values)


@given(dynamic_array_strategy())
def test_pbt_reverse_twice_restores_values(array: DynamicArray[Any]) -> None:
    values = array.to_list()

    array.reverse()
    array.reverse()

    assert array.to_list() == values


@given(
    dynamic_array_and_values_strategy(),
    dynamic_array_and_values_strategy(),
)
def test_pbt_concat_matches_python_list_addition(
    left_pair: tuple[DynamicArray[Any], list[Any]],
    right_pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    left, left_values = left_pair
    right, right_values = right_pair

    result = left.concat(right)

    assert result is left
    assert left.to_list() == left_values + right_values
    assert right.to_list() == right_values


@given(dynamic_array_and_values_strategy())
def test_pbt_monoid_left_identity(
    pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    array, values = pair
    empty: DynamicArray[Any] = DynamicArray.empty()

    result = empty.concat(array)

    assert result is empty
    assert empty.to_list() == values
    assert array.to_list() == values


@given(dynamic_array_and_values_strategy())
def test_pbt_monoid_right_identity(
    pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    array, values = pair
    empty: DynamicArray[Any] = DynamicArray.empty()

    result = array.concat(empty)

    assert result is array
    assert array.to_list() == values
    assert empty.to_list() == []


@given(
    dynamic_array_and_values_strategy(),
    dynamic_array_and_values_strategy(),
    dynamic_array_and_values_strategy(),
)
def test_pbt_monoid_associativity(
    first_pair: tuple[DynamicArray[Any], list[Any]],
    second_pair: tuple[DynamicArray[Any], list[Any]],
    third_pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    first, first_values = first_pair
    second, second_values = second_pair
    third, third_values = third_pair

    left_first = make_array(first_values)
    left_second = make_array(second_values)
    left_third = make_array(third_values)

    right_first = make_array(first_values)
    right_second = make_array(second_values)
    right_third = make_array(third_values)

    left_result = left_first.concat(left_second).concat(left_third)
    right_tail = right_second.concat(right_third)
    right_result = right_first.concat(right_tail)

    expected = first.to_list() + second.to_list() + third.to_list()

    assert left_result.to_list() == expected
    assert right_result.to_list() == expected


@given(dynamic_array_strategy())
def test_pbt_map_identity_preserves_values(array: DynamicArray[Any]) -> None:
    values = array.to_list()

    array.map(lambda value: value)

    assert array.to_list() == values


@given(dynamic_array_strategy())
def test_pbt_filter_always_true_preserves_values(
    array: DynamicArray[Any],
) -> None:
    values = array.to_list()

    array.filter(lambda value: True)

    assert array.to_list() == values


@given(dynamic_array_strategy())
def test_pbt_filter_always_false_removes_all_values(
    array: DynamicArray[Any],
) -> None:
    array.filter(lambda value: False)

    assert array.to_list() == []
    assert array.size() == 0


@given(
    dynamic_array_and_values_strategy(),
    dynamic_array_and_values_strategy(),
)
def test_pbt_eq_matches_python_list_equality(
    first_pair: tuple[DynamicArray[Any], list[Any]],
    second_pair: tuple[DynamicArray[Any], list[Any]],
) -> None:
    first, first_values = first_pair
    second, second_values = second_pair

    assert (first == second) == (first_values == second_values)
