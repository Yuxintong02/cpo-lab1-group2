# group2 - CPO Lab 1 - Variant 2: Dynamic Array

## Description

This repository contains the first laboratory work for the Computational
Process Organization course.

The selected variant is Variant 2: Dynamic array. The project implements a
mutable dynamic array in Python. The data structure stores values in an
internal fixed-capacity block and grows this block when more space is needed.

The implementation uses a Python built-in list as the internal storage block.
The logical size is stored separately from the physical capacity. This is
important because `None` is a valid user value and cannot be used as an
indicator of an empty slot.

## Project structure

Project files:

- `.github/workflows/check.yml`: GitHub Actions checks.
- `.gitignore`: ignored temporary and local files.
- `README.md`: project description, design notes, and analysis.
- `requirements.txt`: project dependencies.
- `dynamic_array.py`: `DynamicArray` implementation.
- `dynamic_array_test.py`: unit tests and property-based tests.

The original template files `foo.py` and `foo_test.py` were removed after the
dynamic array implementation was added.

## Features

Implemented `DynamicArray` features:

- create an empty dynamic array;
- configure the initial capacity;
- configure the growth factor;
- add a value to the end of the array;
- get a value by index;
- set a value by index;
- remove a value by index;
- return the current logical size;
- check whether a value is a member of the array;
- reverse the array in place;
- load values from a Python list;
- convert the dynamic array to a Python list;
- filter values in place by a predicate;
- map values in place by a function;
- reduce values from left to right;
- iterate over values without modifying the array;
- create an empty monoid value;
- concatenate two dynamic arrays.

## Public API

The implemented public API is:

- `DynamicArray(initial_capacity=1, growth_factor=2.0)`:
  create an empty dynamic array.
- `add(value)`:
  append a value to the end of the array.
- `get(index)`:
  return the value at the given index.
- `set(index, value)`:
  replace the value at the given index.
- `remove(index)`:
  remove and return the value at the given index.
- `size()`:
  return the logical number of stored values.
- `member(value)`:
  check whether the value is stored in the array.
- `reverse()`:
  reverse logical values in place.
- `from_list(values)`:
  replace current contents with values from a Python list.
- `to_list()`:
  return logical values as a Python list.
- `filter(predicate)`:
  keep only values accepted by the predicate.
- `map(function)`:
  replace each value with the result of the function.
- `reduce(function, initial_state)`:
  fold values from left to right.
- `__iter__()`:
  return a non-destructive iterator.
- `empty()`:
  return an empty dynamic array.
- `concat(other)`:
  append another dynamic array and return `self`.

## Design notes

### Mutability

The data structure is mutable. Operations that change the structure modify
the current object in place. This applies to `add`, `set`, `remove`,
`reverse`, `from_list`, `filter`, `map`, and `concat`.

The `concat` method is also mutable. It appends values from the right operand
to the current object and returns `self`. The right operand is not modified.

### Internal storage

The implementation uses a Python built-in list as an internal storage block.
This block may be larger than the logical number of stored values.

Valid user values are determined only by indexes lower than the current
logical size. Unused internal slots may contain `None`, but this does not
mean that every `None` value is unused.

### Capacity growth

The constructor accepts `initial_capacity` and `growth_factor`.

Invalid configuration values:

- `initial_capacity < 1` raises `ValueError`;
- `growth_factor <= 1` raises `ValueError`.

When the logical size becomes equal to the current capacity, the array
allocates a larger internal list, copies all logical values to it, and then
adds the new value.

Capacity grows when needed but does not automatically shrink after `remove`
or `filter`.

### Indexing

Only indexes in the range `0 <= index < size()` are valid.

Negative indexes are not supported. Invalid indexes for `get`, `set`, and
`remove` raise `IndexError`.

### `None` values

`None` is allowed as a normal user value. The implementation does not use
`None` checks to determine whether a value is valid. Logical size is the only
source of truth for valid indexes.

### Mixed element types

Mixed element types are allowed. The dynamic array stores arbitrary Python
objects, including integers, strings, booleans, and `None`.

### Mapping and filtering

`map` modifies the current array in place and may change element types.

`filter` modifies the current array in place and keeps only values for which
the predicate returns `True`.

### Iterator behavior

The iterator is non-destructive. Iterating over a dynamic array does not
change its values or size.

## Testing

The project uses unit tests and property-based tests.

### Unit tests

Unit tests cover:

- constructor behavior;
- invalid `initial_capacity`;
- invalid `growth_factor`;
- `size`;
- `to_list`;
- `from_list`;
- `add`;
- resizing when capacity is full;
- `get`;
- `set`;
- `remove` from the first, middle, and last positions;
- invalid indexes;
- `member`;
- `reverse`;
- `map`;
- `filter`;
- `reduce`;
- iterator behavior;
- `empty`;
- `concat`;
- `None` values;
- mixed element types.

### Property-based tests

Property-based tests cover these general properties:

- converting from a Python list and back preserves values;
- dynamic array size equals Python list length;
- reversing twice restores the original values;
- concatenation matches Python list addition;
- empty array is a left identity for concat;
- empty array is a right identity for concat;
- concat is associative by resulting list contents;
- mapping identity preserves values;
- filtering with an always-true predicate preserves values;
- filtering with an always-false predicate produces an empty array.

Generated mixed values include `None`, integers, strings, and booleans.

Because `concat` is mutable, monoid tests create fresh arrays for each side
of each property. This avoids accidental aliasing between mutated objects.

## Contribution

- Yuxintong: project setup, README preparation, implementation workflow,
  local checks, and GitHub Actions validation.
- Yinyutong: design review, testing review, documentation review, and final
  validation support.
- Yuxintong and Yinyutong: API design, corner case discussion, CI fixes, and
  final laboratory review preparation.


## Changelog

### 2026-04-29

- Created the repository from the laboratory template.
- Prepared the local Python virtual environment.
- Installed runtime and development dependencies.
- Verified that the template tests pass locally.
- Drafted the initial README.
- Defined the `DynamicArray` API contract.
- Defined boundary behavior and testing strategy.
- Fixed README formatting for markdown linting.
- Implemented the mutable `DynamicArray`.
- Removed template files `foo.py` and `foo_test.py`.
- Added unit tests for all required operations.
- Fixed style and type-checking issues.
- Added property-based tests with Hypothesis.
- Updated documentation for the final Lab 1 state.

## Analysis and conclusion

The project implements a mutable dynamic array with explicit capacity
management. The main design restriction is that the implementation uses a
Python built-in list internally. This is acceptable for the variant because
the built-in list is used as a fixed-capacity storage block rather than as the
public data structure.

Another restriction is that capacity does not shrink automatically after
removal or filtering. This keeps the implementation simpler and avoids extra
copying, but it may keep more allocated internal space than necessary.

Unit tests are useful for checking concrete examples and specific corner
cases. They make it easy to verify invalid indexes, invalid constructor
arguments, removing from different positions, `None` handling, and resizing.

The disadvantage of unit tests is that they only check the examples that were
written manually. They may miss unexpected combinations of values or operation
sequences.

Property-based tests are useful for checking general invariants over many
generated inputs. In this project, they verify conversion consistency, size
consistency, double reverse, concat behavior, monoid identity, monoid
associativity, identity mapping, and filtering behavior.
