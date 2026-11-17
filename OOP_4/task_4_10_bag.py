"""Задача 4.10 — клас Bag (мультимножина)."""
import pytest


class Bag:
    def __init__(self, items=()):
        self._counts = {}
        try:
            for item in items:
                self._counts[item] = self._counts.get(item, 0) + 1
        except TypeError as e:  # не ітерований аргумент або нехешований елемент
            raise ValueError("Bag створюється з ітерованого набору хешованих елементів") from e

    def __str__(self):
        inner = ", ".join(f"{k}×{c}" for k, c in self._counts.items())
        return f"Bag({inner})"

    def __repr__(self):
        return f"Bag({list(self)!r})"

    def __getitem__(self, item):
        return self._counts.get(item, 0)

    def __setitem__(self, item, n):
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise ValueError("кількість має бути невід'ємним цілим")
        if n == 0:
            self._counts.pop(item, None)
        else:
            self._counts[item] = n

    def __len__(self):
        return sum(self._counts.values())

    def __contains__(self, item):
        try:
            return item in self._counts
        except TypeError:  # нехешований елемент не може бути в Bag
            return False

    def __iter__(self):
        for item, n in self._counts.items():
            for _ in range(n):
                yield item

    def __add__(self, other):
        if not isinstance(other, Bag):
            return NotImplemented
        result = Bag()
        result._counts = dict(self._counts)
        for item, n in other._counts.items():
            result._counts[item] = result._counts.get(item, 0) + n
        return result

    def __eq__(self, other):
        if not isinstance(other, Bag):
            return NotImplemented
        return self._counts == other._counts

    __hash__ = None  # Bag змінюваний


# ---------------------------- тести ----------------------------

def test_getitem_setitem():
    b = Bag(["a", "a", "b"])
    assert b["a"] == 2
    assert b["b"] == 1
    assert b["z"] == 0  # немає — 0
    b["z"] = 5
    assert b["z"] == 5
    b["a"] = 0  # нуль видаляє елемент
    assert b["a"] == 0 and "a" not in b


def test_len_and_contains():
    b = Bag("aab")
    assert len(b) == 3
    assert "a" in b and "c" not in b
    assert len(Bag()) == 0
    assert not Bag()
    b["c"] = 4
    assert len(b) == 7
    assert [] not in b  # нехешований — просто False


def test_iteration_with_repeats():
    b = Bag(["x", "y", "x"])
    assert sorted(b) == ["x", "x", "y"]
    assert sorted(Bag("hello")) == ["e", "h", "l", "l", "o"]
    assert list(Bag()) == []


def test_add_merges_without_mutation():
    a, b = Bag("aab"), Bag("bcc")
    c = a + b
    assert c["a"] == 2 and c["b"] == 2 and c["c"] == 2
    assert len(c) == 6
    assert a == Bag("aab") and b == Bag("bcc")  # операнди не змінились
    assert c is not a


def test_equality():
    assert Bag("aab") == Bag("aba")  # порядок не важливий
    assert Bag("aab") != Bag("ab")
    assert Bag() == Bag()


def test_str_repr():
    b = Bag(["a", "a", "b"])
    assert str(b) == "Bag(a×2, b×1)"
    assert repr(b) == "Bag(['a', 'a', 'b'])"
    assert eval(repr(b)) == b


@pytest.mark.parametrize("n", [-1, 1.5, "2", None, True])
def test_invalid_count(n):
    b = Bag()
    with pytest.raises(ValueError):
        b["a"] = n


def test_invalid_init():
    with pytest.raises(ValueError):
        Bag(5)
    with pytest.raises(ValueError):
        Bag([[1], [2]])  # нехешовані елементи


def test_incompatible_types():
    b = Bag("a")
    with pytest.raises(TypeError):
        b + ["a"]
    with pytest.raises(TypeError):
        b + 1
    assert (b == ["a"]) is False
    with pytest.raises(TypeError):
        hash(b)  # змінюваний об'єкт
