#include <algorithm>
#include <cassert>
#include <iostream>
#include <string>

/** Car models fuel capacity, fuel level and consumption. */
class Car {
    // Основні характеристики автомобіля
    std::string brand_;
    double capacity_;
    double fuel_;
    double consumption_;

public:
    // Створення автомобіля
    Car(
        std::string brand,
        double capacity,
        double fuel,
        double consumption
    ) : brand_(std::move(brand)),
        capacity_(capacity),
        fuel_(fuel),
        consumption_(consumption) {

        assert(capacity >= 0);
        assert(fuel >= 0 && fuel <= capacity);
        assert(consumption > 0);
    }

    // Заправляємо автомобіль
    void refuel(double liters) {
        assert(liters >= 0);

        // Бак не може переповнитися
        fuel_ = std::min(capacity_, fuel_ + liters);
    }

    // Їдемо задану кількість кілометрів
    double drive(double km) {
        assert(km >= 0);

        // Максимальна відстань на наявному пальному
        double possible = fuel_ * 100 / consumption_;

        // Реальна відстань не може бути більшою
        double actual = std::min(km, possible);

        // Витрачаємо відповідну кількість пального
        fuel_ -= actual * consumption_ / 100;

        return actual;
    }

    // Скільки ще можна проїхати
    double range_left() const {
        return fuel_ * 100 / consumption_;
    }
};

void tests() {
    Car a("A", 50, 10, 10);

    // 10 л при витраті 10 л/100 км = 100 км
    assert(a.drive(50) == 50);
    assert(a.range_left() == 50);

    // Пального вистачає тільки на 50 км
    assert(a.drive(100) == 50);

    // Заправка більше місткості не переповнює бак
    a.refuel(100);
    assert(a.range_left() == 500);
}

int main() {
    tests();

    // Незалежні автомобілі
    Car a("BMW", 60, 30, 8);
    Car b("Ford", 50, 10, 10);
    Car c("Audi", 70, 0, 7);

    std::cout << a.drive(100) << ' '
        << a.range_left() << '\n';

    b.refuel(20);

    std::cout << b.range_left() << ' '
        << c.range_left() << '\n';

    std::cout << "Tests passed\n";
}