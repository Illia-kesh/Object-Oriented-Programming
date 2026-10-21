"""Task 2.3: Date with a string constructor and leap-year check."""

import pytest


class Date:
    """A simple date: year, month, day."""

    _DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, year=1970, month=1, day=1):
        """Create a date and validate it."""
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")
        self.year = year
        self.month = month
        if not 1 <= day <= self.days_in_month():
            raise ValueError("Invalid day for this month")
        self.day = day

    @classmethod
    def from_string(cls, text):
        """Create a date from a string in ``YYYY-MM-DD`` format."""
        parts = text.strip().split("-")
        if len(parts) != 3:
            raise ValueError("Expected format YYYY-MM-DD")
        try:
            year, month, day = (int(p) for p in parts)
        except ValueError:
            raise ValueError("Expected format YYYY-MM-DD") from None
        return cls(year, month, day)

    @staticmethod
    def is_leap(year):
        """Return True if the year is a leap year."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def days_in_month(self):
        """Return the number of days in this date's month."""
        if self.month == 2 and Date.is_leap(self.year):
            return 29
        return Date._DAYS[self.month - 1]

    def __str__(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"


def demo():
    d1 = Date.from_string("2024-02-10")
    d2 = Date.from_string("2023-02-10")
    d3 = Date(2026, 10, 20)
    for d in (d1, d2, d3):
        print(d, "-> days in month:", d.days_in_month())
    print("is_leap(2100):", Date.is_leap(2100), "| is_leap(2000):", Date.is_leap(2000))


# ------------------------------- tests ------------------------------------
def test_date_from_string():
    d = Date.from_string("2024-03-15")
    assert (d.year, d.month, d.day) == (2024, 3, 15)


@pytest.mark.parametrize("year,expected", [(2000, True), (1900, False),
                                           (2024, True), (2023, False)])
def test_date_is_leap(year, expected):
    assert Date.is_leap(year) is expected


def test_date_days_in_month():
    assert Date(2024, 2, 1).days_in_month() == 29
    assert Date(2023, 2, 1).days_in_month() == 28
    assert Date(2023, 4, 1).days_in_month() == 30
    assert Date(2023, 12, 31).days_in_month() == 31


@pytest.mark.parametrize("text", ["2024/01/01", "abc", "2024-13-01",
                                  "2023-02-29", "2024-01"])
def test_date_invalid_strings(text):
    with pytest.raises(ValueError):
        Date.from_string(text)


if __name__ == "__main__":
    demo()