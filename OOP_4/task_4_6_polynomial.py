"""Задача 4.6 — клас Polynomial."""
import math
from itertools import zip_longest

import pytest


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _fmt(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


class Polynomial:
    """Коефіцієнти задаються від a0: Polynomial(1, 0, 2) = 1 + 2x^2."""

    def __init__(self, *coeffs):
        if not coeffs:
            raise ValueError("потрібен хоча б один коефіцієнт")
        if not all(_is_number(c) for c in coeffs):
            raise ValueError("коефіцієнти мають бути скінченними числами")
        c = list(coeffs)
        while len(c) > 1 and c[-1] == 0:  # прибираємо старші нулі
            c.pop()
        self._coeffs = tuple(c)

    @property
    def coeffs(self):
        return self._coeffs

    @property
    def degree(self):
        """Степінь (для нульового многочлена — 0)."""
        return len(self._coeffs) - 1

    @staticmethod
    def _coerce(other):
        if isinstance(other, Polynomial):
            return other
        if _is_number(other):
            return Polynomial(other)
        return None

    def __str__(self):
        terms = []
        for i, c in enumerate(self._coeffs):
            if c == 0:
                continue
            a = _fmt(abs(c))
            if i == 0:
                body = a
            else:
                coef = "" if a == "1" else a
                body = f"{coef}x" if i == 1 else f"{coef}x^{i}"
            terms.append(("-" if c < 0 else "+", body))
        if not terms:
            return "0"
        sign, body = terms[0]
        out = ("-" if sign == "-" else "") + body
        for sign, body in terms[1:]:
            out += f" {sign} {body}"
        return out

    def __repr__(self):
        return f"Polynomial({', '.join(repr(c) for c in self._coeffs)})"

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Polynomial(*(a + b for a, b in
                            zip_longest(self._coeffs, o._coeffs, fillvalue=0)))

    __radd__ = __add__

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        result = [0] * (len(self._coeffs) + len(o._coeffs) - 1)
        for i, a in enumerate(self._coeffs):
            for j, b in enumerate(o._coeffs):
                result[i + j] += a * b
        return Polynomial(*result)

    __rmul__ = __mul__

    def __call__(self, x):
        result = 0
        for c in reversed(self._coeffs):  # схема Горнера
            result = result * x + c
        return result

    def __eq__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._coeffs == o._coeffs

    def __hash__(self):
        # узгоджено з __eq__: Polynomial(5) == 5
        return hash(self._coeffs[0]) if self.degree == 0 else hash(self._coeffs)


# ---------------------------- тести ----------------------------

def test_str():
    assert str(Polynomial(1, 0, 2)) == "1 + 2x^2"
    assert str(Polynomial(0, 1)) == "x"
    assert str(Polynomial(-1, -1, 3)) == "-1 - x + 3x^2"
    assert str(Polynomial(0)) == "0"


def test_degree_and_trailing_zeros():
    assert Polynomial(1, 0, 2).degree == 2
    assert Polynomial(1, 2, 0, 0).degree == 1
    assert Polynomial(5).degree == 0
    assert Polynomial(0, 0).degree == 0
    assert Polynomial(1, 2, 0) == Polynomial(1, 2)


def test_call():
    p = Polynomial(1, 0, 2)
    assert p(3) == 19
    assert p(0) == 1
    assert Polynomial(0)(100) == 0


def test_add_and_no_mutation():
    a, b = Polynomial(1, 2), Polynomial(0, 1, 3)
    assert a + b == Polynomial(1, 3, 3)
    assert a == Polynomial(1, 2)
    assert Polynomial(1, 2) + Polynomial(0, -2) == Polynomial(1)  # скорочення
    assert a + 5 == Polynomial(6, 2)
    assert 5 + a == Polynomial(6, 2)


def test_mul():
    assert Polynomial(1, 1) * Polynomial(1, 1) == Polynomial(1, 2, 1)
    assert Polynomial(1, 2) * 3 == Polynomial(3, 6)
    assert 3 * Polynomial(1, 2) == Polynomial(3, 6)
    assert Polynomial(1, 2) * 0 == Polynomial(0)


def test_repr_hash():
    p = Polynomial(1, 0, 2)
    assert repr(p) == "Polynomial(1, 0, 2)"
    assert eval(repr(p)) == p
    assert hash(Polynomial(1, 2)) == hash(Polynomial(1, 2, 0))
    assert Polynomial(5) == 5 and hash(Polynomial(5)) == hash(5)


@pytest.mark.parametrize("args", [(), ("a",), (1, None), (float("nan"),), (True,)])
def test_invalid_init(args):
    with pytest.raises(ValueError):
        Polynomial(*args)


def test_incompatible_types():
    p = Polynomial(1, 2)
    with pytest.raises(TypeError):
        p + "a"
    with pytest.raises(TypeError):
        p * [1]
    with pytest.raises(TypeError):
        "a" + p
    assert (p == "a") is False
