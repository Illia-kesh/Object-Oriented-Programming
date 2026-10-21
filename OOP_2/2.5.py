"""Task 2.5: Config with class-level defaults and per-instance settings."""


class Config:
    """Settings with class-level default values."""

    defaults = {"theme": "light", "language": "uk", "font_size": 14}

    def __init__(self, **settings):
        """Create a config; ``settings`` are this instance's own settings."""
        self.settings = dict(settings)

    def set(self, key, value):
        """Set a value for this instance only."""
        self.settings[key] = value

    def get(self, key):
        """Return the instance value, else the default value, else None."""
        if key in self.settings:
            return self.settings[key]
        return Config.defaults.get(key)


def demo():
    c1 = Config()
    c2 = Config(theme="dark", font_size=18)
    c3 = Config()
    c3.set("language", "en")
    for name, c in (("c1", c1), ("c2", c2), ("c3", c3)):
        print(name, c.get("theme"), c.get("language"), c.get("font_size"))
    c1.set("theme", "blue")
    print("after c1.set(theme=blue): c1 =", c1.get("theme"),
          "| c2 =", c2.get("theme"), "| c3 =", c3.get("theme"))


# ------------------------------- tests ------------------------------------
def test_config_default_value():
    assert Config().get("theme") == "light"


def test_config_instance_overrides_default():
    assert Config(theme="dark").get("theme") == "dark"


def test_config_instances_independent():
    a, b = Config(), Config()
    a.set("theme", "blue")
    assert a.get("theme") == "blue"
    assert b.get("theme") == "light"
    assert Config.defaults["theme"] == "light"


def test_config_missing_key():
    assert Config().get("nope") is None


if __name__ == "__main__":
    demo()