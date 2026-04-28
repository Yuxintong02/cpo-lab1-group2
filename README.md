# group2 - CPO Lab 1 - Variant 2: Dynamic Array

## Description

This repository contains the first laboratory work for the Computational
Process Organization course.

The goal of this work is to design, implement, and test a mutable dynamic
array data structure in Python. The selected variant is Variant 2:
Dynamic array.

The data structure is designed as a mutable object. Operations that change
the structure modify the current object in place whenever applicable. The
implementation will use a Python built-in list as an internal fixed-capacity
storage block. When the logical length becomes equal to the current capacity,
the array will allocate a larger internal block, copy existing elements into
it, and then add the new element.

The implementation must correctly support `None` as a user value.

## Project structure



.github/ workflows/check.yml
.gitignore
README.md
requirements.txt
dynamic_array.py
dynamic_array_test.py


Planned file responsibilities:

- `.github/workflows/check.yml` contains GitHub Actions checks.
- `.gitignore` excludes temporary and local environment files.
- `README.md` describes the project, design decisions, and progress.
- `requirements.txt` lists runtime and testing dependencies.
- `dynamic_array.py` will contain the `DynamicArray` implementation.
- `dynamic_array_test.py` will contain unit tests and property-based tests.

The current template files `foo.py` and `foo_test.py` will be removed after
the dynamic array files are added.

## Features

Planned features for `DynamicArray`:

- create an empty dynamic array with configurable initial capacity;
- use a user-defined growth factor;
- add an element to the end of the array;
- get an element by index;
- set an element by index;
- remove an element by index;
- return the current logical size;
- check membership;
- reverse the array in place;
- load elements from a Python list;
- convert the dynamic array to a Python list;
- filter elements in place by a predicate;
- map elements in place by a function;
- reduce elements from left to right;
- iterate over elements without changing the array;
- create an empty monoid value;
- concatenate two dynamic arrays.

## API design

| Method | Mutable | Planned behavior |
| `DynamicArray(initial_capacity=1, growth_factor=2)` | yes | Create an empty dynamic array. |
| `add(value)` | yes | Append a value to the end and expand if needed. |
| `get(index)` | no | Return the value at `index`. |
| `set(index, value)` | yes | Replace the value at `index`. |
| `remove(index)` | yes | Remove and return the value at `index`. |
| `size()` | no | Return the logical number of stored elements. |
| `member(value)` | no | Check whether `value` is stored in the array. |
| `reverse()` | yes | Reverse logical elements in place. |
| `from_list(values)` | yes | Replace current contents with values from a Python list. |
| `to_list()` | no | Return logical elements as a Python list. |
| `filter(predicate)` | yes | Keep only elements accepted by `predicate`. |
| `map(function)` | yes | Replace each element with `function(element)`. |
| `reduce(function, initial_state)` | no | Fold elements from left to right. |
| `__iter__()` | no | Return a non-destructive iterator. |
| `empty()` | no | Return an empty dynamic array. |
| `concat(other)` | yes | Append elements from `other` and return `self`. |

## Design notes

### Mutability

The data structure is mutable. Methods such as `add`, `set`, `remove`,
`reverse`, `from_list`, `filter`, `map`, and `concat` modify the current
object in place.

For convenience and method chaining, mutating methods return `self`, except
`remove`, which returns the removed value.



### `None` values

`None` is a valid user value. The implementation must not use `None` to
detect whether a cell is occupied. The logical length determines which cells
are part of the array.

### Mixed element types

Mixed element types are allowed. The dynamic array stores arbitrary Python
objects. For example, integers, strings, booleans, and `None` may appear in
the same array.

### Mapping and filtering

`map` modifies elements in place and may change their types. For example, a
mapping function may convert integers to strings.

`filter` modifies the current array in place and keeps only elements for
which the predicate returns `True`.

### Concatenation and monoid behavior

`DynamicArray.empty()` creates an empty dynamic array.

`concat` appends all elements from another dynamic array to the current array
and returns `self`. The right operand is not modified.

The expected monoid properties are:

- identity: `empty.concat(array)` is equivalent to `array`;
- identity: `array.concat(empty)` is equivalent to `array`;
- associativity: `(a.concat(b)).concat(c)` is equivalent to
  `a.concat(b.concat(c))` by resulting list contents.

Because `concat` is mutable, property-based tests will use independent copies
of input arrays to avoid accidental aliasing between test cases.

### Iterator behavior

The iterator must be non-destructive. Iterating over a dynamic array must not
change its contents or size.

## Testing plan

The project will use unit tests and property-based tests.

### Unit tests

Planned unit tests:

- constructor accepts valid configuration values;
- constructor rejects `initial_capacity < 1`;
- constructor rejects `growth_factor <= 1`;
- an empty array has size zero;
- `add` appends one element;
- `add` appends multiple elements in order;
- `add` expands capacity when `length == capacity`;
- `get` returns values by index;
- `get` rejects negative indexes;
- `get` rejects indexes greater than or equal to size;
- `set` replaces values by index;
- `set` rejects invalid indexes;
- `remove` removes and returns values by index;
- `remove` shifts elements after the removed element;
- `remove` rejects invalid indexes;
- `member` finds existing values;
- `member` returns `False` for absent values;
- `reverse` reverses an empty array;
- `reverse` reverses one element;
- `reverse` reverses multiple elements;
- `from_list` replaces previous contents;
- `to_list` returns logical elements only;
- `filter` keeps matching values in place;
- `filter` may produce an empty array;
- `map` changes values in place;
- `map` may change element types;
- `reduce` works for an empty array with an initial state;
- `reduce` works for multiple elements;
- iterator returns elements in order;
- iterator does not modify the array;
- `empty` creates an empty array;
- `concat` appends another array;
- `concat` does not modify the right operand;
- `None` can be added, retrieved, set, removed, and checked by membership;
- mixed types are preserved.

### Property-based tests

Planned property-based tests:

- for any generated list `xs`, `from_list(xs).to_list() == xs`;
- for any generated list `xs`, `from_list(xs).size() == len(xs)`;
- for any generated list `xs`, iterating over the array produces `xs`;
- for any generated list `xs`, `reverse().reverse()` restores `xs`;
- for any generated lists `xs` and `ys`,
  `from_list(xs).concat(from_list(ys)).to_list() == xs + ys`;
- for any generated list `xs`,
  `DynamicArray.empty().concat(from_list(xs)).to_list() == xs`;
- for any generated list `xs`,
  `from_list(xs).concat(DynamicArray.empty()).to_list() == xs`;
- for any generated lists `xs`, `ys`, and `zs`, concat is associative by
  resulting list contents;
- for any generated list `xs`, `map(identity)` preserves `xs`;
- for any generated list `xs`, `filter(lambda _: True)` preserves `xs`;
- for any generated list `xs`, `filter(lambda _: False)` produces an empty
  array;
- for any generated list `xs`, reducing with a counter returns `len(xs)`.

Property-based tests should include integers, strings, booleans, and `None`
where appropriate.

## Contribution

- Yuxintong: planned responsibility for the main `DynamicArray` implementation,
  capacity growth logic, and type annotations.
- Yinyutong: planned responsibility for unit tests, property-based tests, README
  maintenance.



## Changelog

### 2026-04-29

- Created the repository from the laboratory template.
- Prepared the local Python virtual environment.
- Installed runtime and development dependencies.
- Verified that the template tests pass locally.
- Drafted the initial README.
- Defined the planned `DynamicArray` API contract.
- Defined boundary behavior and testing strategy.
