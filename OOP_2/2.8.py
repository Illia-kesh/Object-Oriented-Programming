"""Task 2.8: Person built from a full name."""

import pytest


class Person:
    """A person with a first name and a last name."""

    def __init__(self, first_name, last_name):
        """Create a person."""
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_full_name(cls, full_name):
        """Create an object from a ``"First Last"`` string."""
        parts = full_name.split()
        if len(parts) != 2:
            raise ValueError("Expected exactly two words: first and last name")
        return cls(parts[0], parts[1])

    def full_name(self):
        """Return the full name."""
        return f"{self.first_name} {self.last_name}"

    def initials(self):
        """Return the initials, for example ``І.К.``."""
        return f"{self.first_name[0].upper()}.{self.last_name[0].upper()}."


def demo():
    p1 = Person("Іван", "Коваль")
    p2 = Person.from_full_name("Олена Шевченко")
    for p in (p1, p2):
        print(p.full_name(), "->", p.initials())


# ------------------------------- tests ------------------------------------
def test_person_from_full_name():
    p = Person.from_full_name("Іван Коваль")
    assert (p.first_name, p.last_name) == ("Іван", "Коваль")


def test_person_full_name_and_initials():
    p = Person("Іван", "Коваль")
    assert p.full_name() == "Іван Коваль"
    assert p.initials() == "І.К."


def test_person_initials_lowercase_input():
    assert Person("олена", "шевченко").initials() == "О.Ш."


@pytest.mark.parametrize("text", ["", "Іван", "Іван Петрович Коваль"])
def test_person_invalid_full_name(text):
    with pytest.raises(ValueError):
        Person.from_full_name(text)


if __name__ == "__main__":
    demo()