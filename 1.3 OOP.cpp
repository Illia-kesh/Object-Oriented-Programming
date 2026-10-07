#include <cassert>
#include <iostream>
using namespace std;

/** Counter is a non-negative integer counter. */
class Counter {
    // Поточне значення лічильника
    int count_;

public:
    // Лічильник завжди починається з нуля
    Counter() : count_(0) {}

    // Збільшуємо значення на 1
    void increment() {
        ++count_;
    }

    // Зменшуємо, але не нижче нуля
    void decrement() {
        if (count_ > 0)
            --count_;
    }

    // Повертаємо лічильник до нуля
    void reset() {
        count_ = 0;
    }

    // Повертаємо поточне значення
    int value() const {
        return count_;
    }
};

void tests() {
    Counter a;

    // Початкове значення
    assert(a.value() == 0);

    // Не можна отримати від'ємне значення
    a.decrement();
    assert(a.value() == 0);

    // Перевірка збільшення
    a.increment();
    a.increment();
    assert(a.value() == 2);

    // Перевірка reset
    a.reset();
    assert(a.value() == 0);
}

int main() {
    tests();

    // Об'єкти мають незалежні значення
    Counter a;
    Counter b;
    Counter c;

    a.increment();
    a.increment();
    b.increment();

    cout << a.value() << ' '
        << b.value() << ' '
        << c.value() << '\n';

    cout << "Tests passed\n";
}