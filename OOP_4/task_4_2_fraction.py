"""Задача 4.2 — клас Fraction."""
import math
from functools import total_ordering

import pytest


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


@total_ordering
class Fraction:
    def __init__(self, numerator, denominator=1):
        if not _is_int(numerator) or not _is_int(denominator):
            raise ValueError("чисельник і знаменник мають бути цілими")
        if denominator == 0:
            raise ValueError("знаменник не може бути нулем")
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        g = math.gcd(numerator, denominator)
        self._n = numerator // g
        self._d = denominator // g

    @property
    def numerator(self):
        return self._n

    @property
    def denominator(self):
        return self._d

    @staticmethod
    def _coerce(other):
        if isinstance(other, Fraction):
            return other
        if _is_int(other):
            return Fraction(other)
        return None

    def __str__(self):
        return str(self._n) if self._d == 1 else f"{self._n}/{self._d}"

    def __repr__(self):
        return f"Fraction({self._n}, {self._d})"

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._d + o._n * self._d, self._d * o._d)

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._d - o._n * self._d, self._d * o._d)

    def __rsub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return o - self

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._n, self._d * o._d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        if o._n == 0:
            raise ZeroDivisionError("ділення на нуль")
        return Fraction(self._n * o._d, self._d * o._n)

    def __rtruediv__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return o / self

    def __eq__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._n == o._n and self._d == o._d

    def __lt__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._n * o._d < o._n * self._d

    def __hash__(self):
        # узгоджено з __eq__: Fraction(2) == 2
        return hash(self._n) if self._d == 1 else hash((self._n, self._d))

    def __float__(self):
        return self._n / self._d


# ---------------------------- тести ----------------------------

def test_reduction_and_sign():
    assert str(Fraction(2, 4)) == "1/2"
    assert Fraction(1, -2) == Fraction(-1, 2)
    assert Fraction(0, 5) == Fraction(0, 1)
    assert str(Fraction(6, 3)) == "2"


def test_arithmetic():
    a, b = Fraction(1, 2), Fraction(1, 3)
    assert a + b == Fraction(5, 6)
    assert a - b == Fraction(1, 6)
    assert a * b == Fraction(1, 6)
    assert a / b == Fraction(3, 2)
    assert a == Fraction(1, 2)  # операнд не змінився
    assert 1 + a == Fraction(3, 2)
    assert 1 - a == Fraction(1, 2)
    assert 2 * a == Fraction(1)
    assert 1 / a == Fraction(2)


def test_comparisons_and_sorting():
    a, b = Fraction(1, 3), Fraction(1, 2)
    assert a < b and a <= b and b > a and b >= a and a != b
    assert sorted([b, a, Fraction(-1)]) == [Fraction(-1), a, b]
    assert Fraction(1, 2) < 1


def test_float_and_hash():
    assert float(Fraction(1, 4)) == 0.25
    assert hash(Fraction(2, 4)) == hash(Fraction(1, 2))
    assert len({Fraction(1, 2), Fraction(2, 4)}) == 1
    assert hash(Fraction(3)) == hash(3)


def test_repr():
    f = Fraction(3, 6)
    assert repr(f) == "Fraction(1, 2)"
    assert eval(repr(f)) == f


def test_invalid_init():
    with pytest.raises(ValueError):
        Fraction(1, 0)
    with pytest.raises(ValueError):
        Fraction(1.5, 2)
    with pytest.raises(ValueError):
        Fraction("1", 2)


def test_division_by_zero_fraction():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0)
    with pytest.raises(ZeroDivisionError):
        1 / Fraction(0)


def test_incompatible_types():
    f = Fraction(1, 2)
    with pytest.raises(TypeError):
        f + "a"
    with pytest.raises(TypeError):
        f * 1.5
    with pytest.raises(TypeError):
        f < "a"
    assert (f == "a") is False
