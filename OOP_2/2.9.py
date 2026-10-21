"""Task 2.9: Pizza with method chaining and non-shared toppings."""

import pytest


class Pizza:
    """A pizza of a given size with toppings."""

    BASE_PRICES = {25: 100, 30: 130, 35: 160}
    TOPPING_PRICE = 10

    def __init__(self, size=30, toppings=None):
        """Create a pizza; every object gets its own list of toppings."""
        if size not in Pizza.BASE_PRICES:
            raise ValueError(f"Unknown size: {size}")
        self.size = size
        self.toppings = list(toppings) if toppings else []

    def add(self, topping):
        """Add a topping and return ``self`` (for method chaining)."""
        self.toppings.append(topping)
        return self

    def price(self):
        """Base price for the size + 10 for each topping."""
        return Pizza.BASE_PRICES[self.size] + Pizza.TOPPING_PRICE * len(self.toppings)


def demo():
    z1 = Pizza().add("сир").add("гриби")
    z2 = Pizza(35, ["ковбаса"])
    z3 = Pizza(25)
    print(z1.toppings, z1.price(), "|", z2.toppings, z2.price(), "|",
          z3.toppings, z3.price())


# ------------------------------- tests ------------------------------------
def test_pizza_defaults():
    p = Pizza()
    assert p.size == 30 and p.toppings == [] and p.price() == 130


def test_pizza_chaining_and_price():
    p = Pizza(35).add("сир").add("гриби").add("шинка")
    assert p.toppings == ["сир", "гриби", "шинка"]
    assert p.price() == 160 + 30


def test_pizza_toppings_not_shared():
    a, b = Pizza(), Pizza()
    a.add("сир")
    assert b.toppings == []


def test_pizza_toppings_argument_copied():
    src = ["сир"]
    p = Pizza(25, src)
    p.add("гриби")
    assert src == ["сир"]


def test_pizza_invalid_size():
    with pytest.raises(ValueError):
        Pizza(99)


if __name__ == "__main__":
    demo()