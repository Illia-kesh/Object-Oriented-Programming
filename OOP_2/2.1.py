"""Task 2.1: Employee with a class-level counter."""

import pytest


class Employee:
    """An employee with a name and a salary.

    The class attribute ``count`` tracks how many objects have been created.
    """

    count = 0

    def __init__(self, name, salary=10000):
        """Create an employee.

        :param name: the employee's name
        :param salary: salary (default 10000); must not be negative
        """
        if salary < 0:
            raise ValueError("Salary must not be negative")
        self.name = name
        self.salary = salary
        Employee.count += 1

    def raise_salary(self, percent):
        """Raise the salary by ``percent`` percent.

        :param percent: raise percentage (>= 0)
        :return: the new salary
        """
        if percent < 0:
            raise ValueError("Percent must not be negative")
        self.salary = self.salary * (1 + percent / 100)
        return self.salary


def demo():
    e1, e2, e3 = Employee("Олена"), Employee("Іван", 15000), Employee("Марія", 20000)
    e1.raise_salary(10)
    e2.raise_salary(5)
    print(e1.name, e1.salary, "|", e2.name, e2.salary, "|", e3.name, e3.salary)
    print("Employees created:", Employee.count)


# ------------------------------- tests ------------------------------------
def test_employee_default_salary():
    assert Employee("A").salary == 10000


def test_employee_count_increases():
    before = Employee.count
    Employee("A")
    Employee("B", 500)
    assert Employee.count == before + 2


def test_employee_raise_salary():
    e = Employee("A", 20000)
    assert e.raise_salary(10) == pytest.approx(22000)
    assert e.raise_salary(0) == pytest.approx(22000)


def test_employee_invalid_data():
    with pytest.raises(ValueError):
        Employee("A", -1)
    with pytest.raises(ValueError):
        Employee("A").raise_salary(-5)


if __name__ == "__main__":
    demo()