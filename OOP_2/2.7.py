"""Task 2.7: Money stored in kopecks."""

from decimal import Decimal, InvalidOperation

import pytest


class Money:
    """A sum of money stored in kopecks (an integer)."""

    def __init__(self, kopecks=0):
        """Create a sum from an integer number of kopecks."""
        if isinstance(kopecks, bool) or not isinstance(kopecks, int):
            raise TypeError("Kopecks must be an integer")
        self.kopecks = kopecks

    @classmethod
    def from_float(cls, x):
        """Create a sum from a float number of hryvnias (rounded to kopecks)."""
        return cls(int((Decimal(str(x)) * 100).to_integral_value()))

    @classmethod
    def from_string(cls, text):
        """Create a sum from a string like ``"12.50"`` (a comma is also accepted)."""
        try:
            value = Decimal(text.strip().replace(",", "."))
        except (InvalidOperation, AttributeError):
            raise ValueError(f"Invalid amount: {text!r}") from None
        return cls(int((value * 100).to_integral_value()))

    def to_float(self):
        """Return the sum in hryvnias as a float."""
        return self.kopecks / 100

    def __str__(self):
        sign = "-" if self.kopecks < 0 else ""
        hryvnias, kop = divmod(abs(self.kopecks), 100)
        return f"{sign}{hryvnias}.{kop:02d} грн"


def demo():
    m1 = Money(1250)
    m2 = Money.from_float(12.5)
    m3 = Money.from_string("0.07")
    print(m1, "|", m2, "|", m3, "|", m1.to_float(), "|", m1.kopecks == m2.kopecks)


# ------------------------------- tests ------------------------------------
def test_money_from_float():
    assert Money.from_float(12.5).kopecks == 1250
    assert Money.from_float(0.1 + 0.2).kopecks == 30
    assert Money.from_float(0).kopecks == 0


def test_money_from_string():
    assert Money.from_string("12.50").kopecks == 1250
    assert Money.from_string("12,5").kopecks == 1250
    assert Money.from_string("0.07").kopecks == 7


def test_money_str_and_to_float():
    assert str(Money(1250)) == "12.50 грн"
    assert str(Money(7)) == "0.07 грн"
    assert str(Money(-150)) == "-1.50 грн"
    assert Money(1250).to_float() == 12.5


def test_money_invalid():
    with pytest.raises(TypeError):
        Money(12.5)
    with pytest.raises(ValueError):
        Money.from_string("abc")


if __name__ == "__main__":
    demo()