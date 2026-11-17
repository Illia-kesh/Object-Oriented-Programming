"""Задача 4.1 — клас Vector (2D)."""
import math

import pytest


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


class Vector:
    def __init__(self, x, y):
        if not _is_number(x) or not _is_number(y):
            raise ValueError("координати мають бути скінченними числами")
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return f"({self._x}; {self._y})"

    def __repr__(self):
        return f"Vector({self._x!r}, {self._y!r})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._x - other._x, self._y - other._y)

    def __mul__(self, k):  # v * 3
        if not _is_number(k):
            return NotImplemented
        return Vector(self._x * k, self._y * k)

    def __rmul__(self, k):  # 3 * v
        return self * k

    def __neg__(self):
        return Vector(-self._x, -self._y)

    def __abs__(self):
        return math.hypot(self._x, self._y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("dot() очікує Vector")
        return self._x * other._x + self._y * other._y


# ---------------------------- тести ----------------------------

def test_add_sub_neg():
    a, b = Vector(1, 2), Vector(3, -4)
    assert a + b == Vector(4, -2)
    assert a - b == Vector(-2, 6)
    assert -a == Vector(-1, -2)


def test_mul_both_sides_and_no_mutation():
    v = Vector(1, 2)
    assert v * 3 == Vector(3, 6)
    assert 3 * v == Vector(3, 6)
    assert 0 * v == Vector(0, 0)  # граничний випадок
    assert v == Vector(1, 2)      # операнд не змінився


def test_abs_and_dot():
    assert abs(Vector(3, 4)) == 5
    assert abs(Vector(0, 0)) == 0
    assert Vector(1, 2).dot(Vector(3, 4)) == 11


def test_str_repr():
    v = Vector(1, 2)
    assert str(v) == "(1; 2)"
    assert repr(v) == "Vector(1, 2)"
    assert eval(repr(v)) == v


@pytest.mark.parametrize("x, y", [("a", 1), (1, None), (float("nan"), 0), (True, 1)])
def test_invalid_init(x, y):
    with pytest.raises(ValueError):
        Vector(x, y)


def test_incompatible_types():
    v = Vector(1, 2)
    with pytest.raises(TypeError):
        v + 1
    with pytest.raises(TypeError):
        v * v
    with pytest.raises(TypeError):
        "a" * v
    assert (v == 1) is False
    with pytest.raises(TypeError):
        v.dot(5)
