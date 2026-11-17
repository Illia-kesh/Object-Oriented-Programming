"""Задача 4.8 — клас Version."""
import re
from functools import total_ordering

import pytest

_PATTERN = re.compile(r"\d+(\.\d+)*")


@total_ordering
class Version:
    def __init__(self, text):
        if not isinstance(text, str) or not _PATTERN.fullmatch(text.strip()):
            raise ValueError(f"некоректна версія: {text!r}")
        self._parts = tuple(int(p) for p in text.strip().split("."))

    @property
    def _key(self):
        # кінцеві нулі не впливають на порівняння: 1.2 == 1.2.0
        k = list(self._parts)
        while len(k) > 1 and k[-1] == 0:
            k.pop()
        return tuple(k)

    def __str__(self):
        return ".".join(map(str, self._parts))

    def __repr__(self):
        return f"Version({str(self)!r})"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._key == other._key

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._key < other._key  # порівняння кортежів чисел

    def __hash__(self):
        return hash(self._key)


# ---------------------------- тести ----------------------------

def test_numeric_comparison():
    assert Version("1.2.10") > Version("1.2.9")  # не рядкове порівняння
    assert Version("1.10") > Version("1.9")
    assert Version("2.0") > Version("1.99.99")
    assert Version("1.0") <= Version("1.0") and Version("1.0") >= Version("1.0")


def test_equality_and_hash():
    assert Version("1.2") == Version("1.2.0")
    assert Version("1.2") != Version("1.2.1")
    assert hash(Version("1.2")) == hash(Version("1.2.0"))
    assert len({Version("1.0"), Version("1.0.0"), Version("1")}) == 1


def test_sorted():
    versions = [Version(v) for v in ["1.2.10", "1.2.9", "1.10", "1.2", "0.9"]]
    assert [str(v) for v in sorted(versions)] == ["0.9", "1.2", "1.2.9", "1.2.10", "1.10"]
    assert max(versions) == Version("1.10")


def test_str_repr():
    v = Version("1.2.10")
    assert str(v) == "1.2.10"
    assert repr(v) == "Version('1.2.10')"
    assert eval(repr(v)) == v
    assert str(Version(" 01.2 ")) == "1.2"
    assert str(Version("7")) == "7"  # одна компонента


@pytest.mark.parametrize("text", ["", "1..2", "a.b", "1.2-beta", "1.", ".1", None, 12, "1 2"])
def test_invalid_init(text):
    with pytest.raises(ValueError):
        Version(text)


def test_incompatible_types():
    v = Version("1.0")
    with pytest.raises(TypeError):
        v < "1.1"
    with pytest.raises(TypeError):
        v > 2
    assert (v == "1.0") is False
    assert (v == 1) is False
