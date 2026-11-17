"""Задача 4.5 — клас Complex."""
import math

import pytest


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _fmt(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


class Complex:
    def __init__(self, re=0, im=0):
        if not _is_number(re) or not _is_number(im):
            raise ValueError("re та im мають бути скінченними числами")
        self._re = re
        self._im = im

    @property
    def re(self):
        return self._re

    @property
    def im(self):
        return self._im

    @staticmethod
    def _coerce(other):
        if isinstance(other, Complex):
            return other
        if _is_number(other):
            return Complex(other)
        return None

    def __str__(self):
        sign = "-" if self._im < 0 else "+"
        return f"{_fmt(self._re)}{sign}{_fmt(abs(self._im))}i"

    def __repr__(self):
        return f"Complex({self._re!r}, {self._im!r})"

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(self._re + o._re, self._im + o._im)

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(self._re - o._re, self._im - o._im)

    def __rsub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return o - self

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(self._re * o._re - self._im * o._im,
                       self._re * o._im + self._im * o._re)

    __rmul__ = __mul__

    def __neg__(self):
        return Complex(-self._re, -self._im)

    def __abs__(self):
        return math.hypot(self._re, self._im)

    def conjugate(self):
        return Complex(self._re, -self._im)

    def __eq__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._re == o._re and self._im == o._im

    def __hash__(self):
        # узгоджено з __eq__: Complex(2) == 2
        return hash(self._re) if self._im == 0 else hash((self._re, self._im))


# ---------------------------- тести ----------------------------

def test_add_sub():
    a, b = Complex(1, 2), Complex(3, -1)
    assert a + b == Complex(4, 1)
    assert a - b == Complex(-2, 3)
    assert a == Complex(1, 2)  # операнд не змінився


def test_mul():
    assert Complex(1, 2) * Complex(3, 4) == Complex(-5, 10)
    assert Complex(0, 1) * Complex(0, 1) == Complex(-1, 0)
    assert Complex(1, 2) * Complex() == Complex()  # множення на нуль


def test_abs_conjugate():
    assert abs(Complex(3, 4)) == 5
    assert abs(Complex()) == 0
    assert Complex(1, 2).conjugate() == Complex(1, -2)


def test_real_numbers_both_sides():
    c = Complex(1, 2)
    assert c + 2 == Complex(3, 2)
    assert 2 + c == Complex(3, 2)
    assert 5 - c == Complex(4, -2)
    assert c - 1 == Complex(0, 2)
    assert 2 * c == Complex(2, 4)
    assert c * 0.5 == Complex(0.5, 1.0)


def test_eq_with_real_and_hash():
    assert Complex(2, 0) == 2
    assert Complex(2, 1) != 2
    assert hash(Complex(2)) == hash(2)
    assert len({Complex(1, 2), Complex(1, 2)}) == 1


def test_str_repr():
    assert str(Complex(1, 2)) == "1+2i"
    assert str(Complex(1, -2)) == "1-2i"
    assert str(Complex()) == "0+0i"
    c = Complex(1.5, -2)
    assert eval(repr(c)) == c


@pytest.mark.parametrize("re, im", [("a", 0), (0, None), (float("nan"), 0), (True, 0)])
def test_invalid_init(re, im):
    with pytest.raises(ValueError):
        Complex(re, im)


def test_incompatible_types():
    c = Complex(1, 1)
    with pytest.raises(TypeError):
        c + "a"
    with pytest.raises(TypeError):
        "a" + c
    with pytest.raises(TypeError):
        c * [1]
    assert (c == "a") is False
