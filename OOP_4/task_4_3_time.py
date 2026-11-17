"""Задача 4.3 — клас Time."""
from functools import total_ordering

import pytest


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


@total_ordering
class Time:
    def __init__(self, hours=0, minutes=0, seconds=0):
        for v in (hours, minutes, seconds):
            if not _is_int(v) or v < 0:
                raise ValueError("години, хвилини й секунди — невід'ємні цілі")
        self._total = hours * 3600 + minutes * 60 + seconds  # нормалізація

    @classmethod
    def _from_seconds(cls, total):
        return cls(0, 0, total)

    @property
    def hours(self):
        return self._total // 3600

    @property
    def minutes(self):
        return self._total % 3600 // 60

    @property
    def seconds(self):
        return self._total % 60

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def __repr__(self):
        return f"Time({self.hours}, {self.minutes}, {self.seconds})"

    def __add__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return Time._from_seconds(self._total + other._total)

    def __sub__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return Time._from_seconds(max(0, self._total - other._total))

    def __eq__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return self._total == other._total

    def __lt__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return self._total < other._total

    def __hash__(self):
        return hash(self._total)


# ---------------------------- тести ----------------------------

def test_normalization_and_str():
    t = Time(1, 75, 130)  # 1:75:130 -> 02:17:10
    assert (t.hours, t.minutes, t.seconds) == (2, 17, 10)
    assert str(t) == "02:17:10"
    assert str(Time()) == "00:00:00"


def test_add():
    a, b = Time(0, 59, 59), Time(0, 0, 1)
    assert a + b == Time(1, 0, 0)
    assert str(a + b) == "01:00:00"
    assert a == Time(0, 59, 59)  # операнд не змінився


def test_sub_floor_at_zero():
    assert Time(2, 0, 0) - Time(0, 30, 0) == Time(1, 30, 0)
    assert Time(0, 1, 0) - Time(1, 0, 0) == Time(0, 0, 0)  # не нижче 0


def test_comparisons_and_sorting():
    a, b = Time(0, 1, 0), Time(0, 0, 61)
    assert a < b and b > a and a <= b and a != b
    assert Time(0, 0, 60) == Time(0, 1, 0)
    assert sorted([Time(1), Time(0, 5), Time(0, 0, 3)]) == [Time(0, 0, 3), Time(0, 5), Time(1)]


def test_hash_consistent_with_eq():
    assert hash(Time(0, 1, 0)) == hash(Time(0, 0, 60))
    assert len({Time(0, 1, 0), Time(0, 0, 60)}) == 1


def test_repr():
    t = Time(1, 2, 3)
    assert repr(t) == "Time(1, 2, 3)"
    assert eval(repr(t)) == t


@pytest.mark.parametrize("args", [(-1,), (0, -5), (0, 0, -1), (1.5,), ("1",), (True,)])
def test_invalid_init(args):
    with pytest.raises(ValueError):
        Time(*args)


def test_incompatible_types():
    t = Time(1)
    with pytest.raises(TypeError):
        t + 5
    with pytest.raises(TypeError):
        t - "a"
    with pytest.raises(TypeError):
        t < 5
    assert (t == 3600) is False
