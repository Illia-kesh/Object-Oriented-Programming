"""Task 2.2: Temperature with alternative constructors."""

import pytest


class Temperature:
    """A temperature in degrees Celsius."""

    ABSOLUTE_ZERO = -273.15

    def __init__(self, celsius=0.0):
        """Create a temperature; values below absolute zero are rejected."""
        if not Temperature.is_valid(celsius):
            raise ValueError("Temperature is below absolute zero")
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f):
        """Create an object from a value in degrees Fahrenheit."""
        return cls((f - 32) * 5 / 9)

    @classmethod
    def from_kelvin(cls, k):
        """Create an object from a value in kelvins."""
        return cls(k - 273.15)

    def to_fahrenheit(self):
        """Return the temperature in degrees Fahrenheit."""
        return self.celsius * 9 / 5 + 32

    @staticmethod
    def is_valid(c):
        """Check that a Celsius temperature is not below absolute zero."""
        return c >= Temperature.ABSOLUTE_ZERO


def demo():
    t1 = Temperature(25)
    t2 = Temperature.from_fahrenheit(212)
    t3 = Temperature.from_kelvin(0)
    print(t1.celsius, "C =", t1.to_fahrenheit(), "F")
    print(t2.celsius, "C;", t3.celsius, "C")
    print("is_valid(-300):", Temperature.is_valid(-300))


# ------------------------------- tests ------------------------------------
def test_temperature_from_fahrenheit():
    assert Temperature.from_fahrenheit(212).celsius == pytest.approx(100)
    assert Temperature.from_fahrenheit(32).celsius == pytest.approx(0)


def test_temperature_from_kelvin_and_to_fahrenheit():
    assert Temperature.from_kelvin(273.15).celsius == pytest.approx(0)
    assert Temperature(100).to_fahrenheit() == pytest.approx(212)


def test_temperature_is_valid_boundary():
    assert Temperature.is_valid(-273.15)
    assert not Temperature.is_valid(-273.16)


def test_temperature_invalid_raises():
    with pytest.raises(ValueError):
        Temperature(-300)
    with pytest.raises(ValueError):
        Temperature.from_kelvin(-1)


if __name__ == "__main__":
    demo()