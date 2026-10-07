#include <cassert>
#include <iostream>
using namespace std;

/** LightSwitch stores an on/off state and toggle count. */
class LightSwitch {
    // Стан вимикача
    bool on_;

    // Кількість перемикань
    int count_;

public:
    // За замовчуванням вимикач вимкнений
    LightSwitch(bool on = false)
        : on_(on), count_(0) {
    }

    // Змінюємо стан на протилежний
    void toggle() {
        on_ = !on_;
        ++count_;
    }

    // Перевіряємо стан
    bool is_on() const {
        return on_;
    }

    // Повертаємо кількість перемикань
    int switches() const {
        return count_;
    }
};

void tests() {
    LightSwitch a;

    assert(!a.is_on());
    assert(a.switches() == 0);

    // Перше перемикання
    a.toggle();

    assert(a.is_on());
    assert(a.switches() == 1);

    // Друге перемикання
    a.toggle();

    assert(!a.is_on());
    assert(a.switches() == 2);
}

int main() {
    tests();

    // Незалежні вимикачі
    LightSwitch a;
    LightSwitch b(true);
    LightSwitch c;

    a.toggle();
    a.toggle();
    b.toggle();

    cout << a.is_on() << '/'
        << a.switches() << '\n';

    cout << b.is_on() << '/'
        << b.switches() << '\n';

    cout << c.is_on() << '/'
        << c.switches() << '\n';

    cout << "Tests passed\n";
}