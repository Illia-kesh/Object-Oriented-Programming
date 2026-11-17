"""Задача 4.9 — клас Money."""
import math
from functools import total_ordering

import pytest


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


@total_ordering
class Money:
    """Сума в копійках (цілі) та валюта. Від'ємні значення дозволені (борг)."""

    def __init__(self, kopecks, currency="UAH"):
        if not _is_int(kopecks):
            raise ValueError("сума має бути цілою кількістю копійок")
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("валюта має бути непорожнім рядком")
        self._k = kopecks
        self._cur = currency.strip().upper()

    @property
    def kopecks(self):
        return self._k

    @property
    def currency(self):
        return self._cur

    def _check_same_currency(self, other):
        if self._cur != other._cur:
            raise ValueError(f"різні валюти: {self._cur} і {other._cur}")

    def __str__(self):
        sign = "-" if self._k < 0 else ""
        units, cents = divmod(abs(self._k), 100)
        return f"{sign}{units}.{cents:02d} {self._cur}"

    def __repr__(self):
        return f"Money({self._k!r}, {self._cur!r})"

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same_currency(other)
        return Money(self._k + other._k, self._cur)

    def __radd__(self, other):
        # дає змогу sum([...]): перший доданок — 0
        if _is_int(other) and other == 0:
            return self
        return NotImplemented

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same_currency(other)
        return Money(self._k - other._k, self._cur)

    def __mul__(self, k):
        if not _is_number(k):
            return NotImplemented
        return Money(round(self._k * k), self._cur)  # округлення до копійки

    __rmul__ = __mul__

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self._k == other._k and self._cur == other._cur

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same_currency(other)
        return self._k < other._k

    def __hash__(self):
        return hash((self._k, self._cur))

    def __bool__(self):
        return self._k != 0


# ---------------------------- тести ----------------------------

def test_add_sub():
    a, b = Money(1050), Money(250)
    assert a + b == Money(1300)
    assert a - b == Money(800)
    assert b - a == Money(-800)
    assert a == Money(1050)  # операнд не змінився


def test_different_currency_value_error():
    with pytest.raises(ValueError):
        Money(100, "UAH") + Money(100, "USD")
    with pytest.raises(ValueError):
        Money(100, "UAH") - Money(100, "USD")
    with pytest.raises(ValueError):
        Money(100, "UAH") < Money(100, "USD")
    assert Money(100, "UAH") != Money(100, "USD")  # == не кидає виняток


def test_mul_and_rounding():
    m = Money(1000)
    assert m * 3 == Money(3000)
    assert 3 * m == Money(3000)
    assert m * 0 == Money(0)
    assert m * 0.155 == Money(155)
    assert Money(101) * 0.5 == Money(50)  # 50.5 -> 50 (banker's rounding)


def test_comparisons_and_sorting():
    a, b = Money(100), Money(200)
    assert a < b and a <= b and b > a and b >= a and a != b
    assert sorted([b, a, Money(-5)]) == [Money(-5), a, b]


def test_bool():
    assert not Money(0)
    assert Money(1)
    assert Money(-1)


def test_sum_via_radd():
    items = [Money(100), Money(250), Money(50)]
    assert sum(items) == Money(400)
    assert sum([Money(100)]) == Money(100)
    assert sum([]) == 0
    assert 0 + Money(5) == Money(5)


def test_str_repr_hash():
    assert str(Money(1234)) == "12.34 UAH"
    assert str(Money(5, "usd")) == "0.05 USD"
    assert str(Money(-1205)) == "-12.05 UAH"
    m = Money(1234, "USD")
    assert repr(m) == "Money(1234, 'USD')"
    assert eval(repr(m)) == m
    assert len({Money(1), Money(1)}) == 1


@pytest.mark.parametrize("args", [(1.5,), ("10",), (True,), (100, ""), (100, None), (100, 5)])
def test_invalid_init(args):
    with pytest.raises(ValueError):
        Money(*args)


def test_incompatible_types():
    m = Money(100)
    with pytest.raises(TypeError):
        m + 5
    with pytest.raises(TypeError):
        5 + m  # лише 0 дозволено
    with pytest.raises(TypeError):
        m - 1
    with pytest.raises(TypeError):
        m * "a"
    with pytest.raises(TypeError):
        m * m
    with pytest.raises(TypeError):
        m < 5
    assert (m == 100) is False
