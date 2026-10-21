"""Task 2.4: MathUtils with static methods only."""

import pytest


class MathUtils:
    """A collection of math functions (static methods only)."""

    @staticmethod
    def gcd(a, b):
        """Greatest common divisor (Euclid's algorithm)."""
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def is_prime(n):
        """Return True if n is a prime number."""
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    @staticmethod
    def factorial(n):
        """Factorial of n (n >= 0)."""
        if n < 0:
            raise ValueError("Factorial is defined for n >= 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def fibonacci(n):
        """The n-th Fibonacci number (F0 = 0, F1 = 1)."""
        if n < 0:
            raise ValueError("n must be >= 0")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a


def demo():
    print("gcd(48, 18) =", MathUtils.gcd(48, 18))
    print("is_prime:", [n for n in range(20) if MathUtils.is_prime(n)])
    print("factorial(5) =", MathUtils.factorial(5))
    print("fibonacci(0..10):", [MathUtils.fibonacci(i) for i in range(11)])


# ------------------------------- tests ------------------------------------
def test_gcd():
    assert MathUtils.gcd(48, 18) == 6
    assert MathUtils.gcd(0, 5) == 5
    assert MathUtils.gcd(7, 13) == 1


def test_is_prime():
    assert [n for n in range(15) if MathUtils.is_prime(n)] == [2, 3, 5, 7, 11, 13]
    assert not MathUtils.is_prime(-7)
    assert MathUtils.is_prime(97)


def test_factorial():
    assert MathUtils.factorial(0) == 1
    assert MathUtils.factorial(5) == 120
    with pytest.raises(ValueError):
        MathUtils.factorial(-1)


def test_fibonacci():
    assert [MathUtils.fibonacci(i) for i in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13]
    with pytest.raises(ValueError):
        MathUtils.fibonacci(-1)


if __name__ == "__main__":
    demo()