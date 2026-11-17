"""Задача 4.4 — клас Matrix."""
import math

import pytest


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


class Matrix:
    def __init__(self, rows):
        if not isinstance(rows, (list, tuple)) or not rows:
            raise ValueError("матриця має бути непорожнім списком рядків")
        for r in rows:
            if not isinstance(r, (list, tuple)) or not r:
                raise ValueError("кожен рядок має бути непорожнім списком")
        if len({len(r) for r in rows}) != 1:
            raise ValueError("усі рядки мають мати однакову довжину")
        if not all(_is_number(v) for r in rows for v in r):
            raise ValueError("елементи мають бути скінченними числами")
        self._rows = tuple(tuple(r) for r in rows)

    @property
    def shape(self):
        return len(self._rows), len(self._rows[0])

    def __str__(self):
        return "\n".join(" ".join(str(v) for v in r) for r in self._rows)

    def __repr__(self):
        return f"Matrix({[list(r) for r in self._rows]!r})"

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError("розміри матриць не збігаються")
        return Matrix([[a + b for a, b in zip(r1, r2)]
                       for r1, r2 in zip(self._rows, other._rows)])

    def __mul__(self, other):
        if _is_number(other):
            return Matrix([[v * other for v in r] for r in self._rows])
        if isinstance(other, Matrix):
            if self.shape[1] != other.shape[0]:
                raise ValueError("кількість стовпців першої ≠ кількості рядків другої")
            cols = list(zip(*other._rows))
            return Matrix([[sum(a * b for a, b in zip(r, c)) for c in cols]
                           for r in self._rows])
        return NotImplemented

    def __rmul__(self, other):  # 3 * m
        if _is_number(other):
            return self * other
        return NotImplemented

    def __getitem__(self, key):
        if isinstance(key, tuple):  # m[i, j]
            if len(key) != 2:
                raise TypeError("очікується m[i, j]")
            i, j = key
            return self._rows[i][j]
        if isinstance(key, int) and not isinstance(key, bool):  # m[i][j]
            return self._rows[key]
        raise TypeError("індекс має бути int або кортеж (i, j)")

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._rows == other._rows

    def __hash__(self):
        return hash(self._rows)


# ---------------------------- тести ----------------------------

def test_add_and_no_mutation():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[10, 20], [30, 40]])
    assert a + b == Matrix([[11, 22], [33, 44]])
    assert a == Matrix([[1, 2], [3, 4]])


def test_scalar_mul_both_sides():
    m = Matrix([[1, 2], [3, 4]])
    assert m * 2 == Matrix([[2, 4], [6, 8]])
    assert 2 * m == Matrix([[2, 4], [6, 8]])
    assert 0 * m == Matrix([[0, 0], [0, 0]])


def test_matrix_mul():
    a = Matrix([[1, 2, 3], [4, 5, 6]])      # 2x3
    b = Matrix([[7, 8], [9, 10], [11, 12]])  # 3x2
    assert a * b == Matrix([[58, 64], [139, 154]])
    assert (a * b).shape == (2, 2)
    with pytest.raises(ValueError):
        a * a


def test_indexing():
    m = Matrix([[1, 2], [3, 4]])
    assert m[0, 1] == 2
    assert m[1, 0] == 3
    assert m[1][1] == 4
    assert m[-1, -1] == 4
    with pytest.raises(IndexError):
        m[2, 0]
    with pytest.raises(TypeError):
        m[0, 1, 2]
    with pytest.raises(TypeError):
        m["a"]


def test_size_checks():
    with pytest.raises(ValueError):
        Matrix([[1, 2]]) + Matrix([[1], [2]])


def test_str_repr_eq():
    m = Matrix([[1, 2], [3, 4]])
    assert str(m) == "1 2\n3 4"
    assert repr(m) == "Matrix([[1, 2], [3, 4]])"
    assert eval(repr(m)) == m
    assert m != Matrix([[1, 2], [3, 5]])


@pytest.mark.parametrize("rows", [[], [[]], [[1, 2], [3]], [[1, "a"]], "abc", [1, 2], [[float("inf")]]])
def test_invalid_init(rows):
    with pytest.raises(ValueError):
        Matrix(rows)


def test_incompatible_types():
    m = Matrix([[1]])
    with pytest.raises(TypeError):
        m + 1
    with pytest.raises(TypeError):
        m * "a"
    with pytest.raises(TypeError):
        "a" * m
    assert (m == [[1]]) is False
