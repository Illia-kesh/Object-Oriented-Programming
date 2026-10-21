"""Task 2.10: Registry keeping all instances at class level."""

import pytest


class Registry:
    """A named object; all created instances are stored at class level."""

    _instances = []

    def __init__(self, name):
        """Create an object and register it."""
        self.name = name
        Registry._instances.append(self)

    @classmethod
    def all(cls):
        """Return a list (copy) of all registered instances."""
        return list(cls._instances)

    @classmethod
    def find(cls, name):
        """Return the first instance with this name, or None."""
        for obj in cls._instances:
            if obj.name == name:
                return obj
        return None

    @classmethod
    def clear(cls):
        """Clear the registry."""
        cls._instances.clear()


def demo():
    Registry.clear()
    r1, r2, r3 = Registry("alpha"), Registry("beta"), Registry("gamma")
    print("all:", [r.name for r in Registry.all()])
    print("find('beta') is r2:", Registry.find("beta") is r2,
          "| find('x'):", Registry.find("x"))
    Registry.clear()
    print("after clear:", Registry.all())


# ------------------------------- tests ------------------------------------
@pytest.fixture(autouse=True)
def _clean_registry():
    Registry.clear()
    yield
    Registry.clear()


def test_registry_all():
    a, b = Registry("a"), Registry("b")
    assert Registry.all() == [a, b]


def test_registry_find():
    a, b = Registry("a"), Registry("b")
    assert Registry.find("b") is b
    assert Registry.find("zzz") is None


def test_registry_clear():
    Registry("a")
    Registry.clear()
    assert Registry.all() == []
    assert Registry.find("a") is None


def test_registry_all_returns_copy():
    Registry("a")
    Registry.all().clear()
    assert len(Registry.all()) == 1


if __name__ == "__main__":
    demo()