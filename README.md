# group2 - CPO Lab 1 - Variant 2: Dynamic Array

## Description

This repository contains the first laboratory work for the Computational
Process Organization course.

The goal is to design, implement, and test a mutable dynamic array in Python.
The selected variant is Variant 2: Dynamic array.

The data structure is designed as a mutable object. Operations that change
the structure should modify the current object in place when applicable.

The implementation will use a Python built-in list as an internal
fixed-capacity storage block. When length becomes equal to capacity, the
array will allocate a larger block, copy existing elements, and add the new
element.

The implementation must correctly support `None` as a user value.

## Project structure

Planned project files:

- `.github/workflows/check.yml`: GitHub Actions checks.
- `.gitignore`: ignored temporary and local files.
- `README.md`: project description and design notes.
- `requirements.txt`: project dependencies.
- `dynamic_array.py`: planned dynamic array implementation.
- `dynamic_array_test.py`: planned tests.

The template files `foo.py` and `foo_test.py` will be removed after the
dynamic array files are added.

## Features

Planned features:

- create an empty dynamic array;
- configure the initial capacity;
- configure the growth factor;
- add an element to the end;
- get an element by index;
- set an element by index;
- remove an element by index;
- return the current logical size;
- check membership;
- reverse the array in place;
- load values from a Python list;
- convert the structure to a Python list;
- filter elements in place;
- map elements in place;
- reduce elements from left to right;
- iterate over elements without changing the array;
- create an empty monoid value;
- concatenate two dynamic arrays.

## API design

Planned public API:

- `DynamicArray(initial_capacity=1, growth_factor=2)`:
  create an empty array.
- `add(value)`:
  append a value and return `self`.
- `get(index)`:
  return the value at the given index.
- `set(index, value)`:
  replace a value and return `self`.
- `remove(index)`:
  remove and return the value at the given index.
- `size()`:
  return the logical number of stored elements.
- `member(value)`:
  check whether the value is stored in the array.
- `reverse()`:
  reverse logical elements in place and return `self`.
- `from_list(values)`:
  replace current contents and return `self`.
- `to_list()`:
  return logical elements as a Python list.
- `filter(predicate)`:
  keep matching elements and return `self`.
- `map(function)`:
  replace each element and return `self`.
- `reduce(function, initial_state)`:
  fold elements from left to right.
- `__iter__()`:
  return a non-destructive iterator.
- `empty()`:
  return an empty dynamic array.
- `concat(other)`:
  append another array and return `self`.

## Design notes

### Mutability

The structure is mutable. Methods such as `add`, `set`, `remove`, `reverse`,
`from_list`, `filter`, `map`, and `concat` modify the current object in place.

Mutating methods return `self` for convenient chaining, except `remove`,
which returns the removed value.

### Internal storage

The implementation will use a Python built-in list as an internal storage
block. The internal capacity may be larger than the logical length.

Only indexes in the range `0 <= index < length` are valid.

### Capacity growth

The constructor accepts `initial_capacity` and `growth_factor`.

Invalid configuration values:

- `initial_capacity < 1` raises `ValueError`;
- `growth_factor <= 1` raises `ValueError`.

When `length == capacity`, the array allocates a larger internal block and
copies existing logical elements into it.

### Indexing

Negative indexes are not supported. Invalid indexes for `get`, `set`, and
`remove` raise `IndexError`.

### `None` values

`None` is a valid user value. The implementation must not use `None` to
detect whether a cell is occupied. Logical length defines valid elements.

### Mixed element types

Mixed element types are allowed. The array stores arbitrary Python objects,
including integers, strings, booleans, and `None`.

### Mapping and filtering

`map` modifies elements in place and may change their types.

`filter` modifies the current array in place and keeps only elements for
which the predicate returns `True`.

### Concatenation and monoid behavior

`DynamicArray.empty()` creates an empty dynamic array.

`concat` appends all elements from another dynamic array to the current array
and returns `self`. The right operand is not modified.

Expected monoid properties:

- left identity: `empty.concat(array)` is equivalent to `array`;
- right identity: `array.concat(empty)` is equivalent to `array`;
- associativity: `(a.concat(b)).concat(c)` and `a.concat(b.concat(c))`
  produce equivalent list contents.

Because `concat` is mutable, tests will use independent copies of arrays.

### Iterator behavior

The iterator must be non-destructive. Iterating over an array must not change
its contents or size.

## Testing plan

The project will use unit tests and property-based tests.

### Unit tests

Planned unit tests:

- constructor accepts valid values;
- constructor rejects `initial_capacity < 1`;
- constructor rejects `growth_factor <= 1`;
- an empty array has size zero;
- `add` appends one element;
- `add` appends multiple elements in order;
- `add` expands capacity when needed;
- `get` returns values by index;
- `get` rejects invalid indexes;
- `set` replaces values by index;
- `set` rejects invalid indexes;
- `remove` removes and returns values;
- `remove` shifts following elements left;
- `remove` rejects invalid indexes;
- `member` finds existing values;
- `member` rejects absent values;
- `reverse` works for empty, one-element, and multi-element arrays;
- `from_list` replaces previous contents;
- `to_list` returns logical elements only;
- `filter` keeps matching values in place;
- `filter` may produce an empty array;
- `map` changes values in place;
- `map` may change element types;
- `reduce` works with an initial state;
- iterator returns elements in order;
- iterator does not modify the array;
- `empty` creates an empty array;
- `concat` appends another array;
- `concat` does not modify the right operand;
- `None` can be added, retrieved, set, removed, and checked;
- mixed types are preserved.

### Property-based tests

Planned property-based tests:

- `from_list(xs).to_list() == xs`;
- `from_list(xs).size() == len(xs)`;
- iteration over the array produces `xs`;
- double reverse restores `xs`;
- concatenation produces `xs + ys`;
- empty is a left identity;
- empty is a right identity;
- concat is associative by resulting list contents;
- `map(identity)` preserves `xs`;
- `filter(lambda _: True)` preserves `xs`;
- `filter(lambda _: False)` produces an empty array;
- reducing with a counter returns `len(xs)`.

Generated test values should include integers, strings, booleans, and `None`.

## Contribution

- Alice: planned responsibility for the main implementation, capacity growth
  logic, and type annotations.
- Bob: planned responsibility for unit tests, property-based tests, and
  README maintenance.

The final contribution section must stay consistent with the real Git history
and should be updated before submission.

## Changelog

### 2026-04-29

- Created the repository from the laboratory template.
- Prepared the local Python virtual environment.
- Installed runtime and development dependencies.
- Verified that the template tests pass locally.
- Drafted the initial README.
- Defined the planned `DynamicArray` API contract.
- Defined boundary behavior and testing strategy.
- Fixed README formatting for markdown linting.

## Analysis and conclusion

This project will implement a mutable dynamic array with explicit capacity
management. The main implementation risk is confusing logical length with
physical capacity, especially because `None` is a valid user value.

Unit tests will check specific corner cases, such as invalid indexes,
capacity expansion, and `None` handling. Property-based tests will check
general invariants, such as list conversion consistency, size consistency,
monoid identity, and monoid associativity.

At this stage, the project is prepared but the full implementation has not
started yet.
