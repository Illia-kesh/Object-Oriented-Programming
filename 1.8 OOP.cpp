#include <cassert>
#include <iostream>
#include <string>
using namespace std;

/** Product stores a name, price and percentage discount. */
class Product {
    // Дані товару
    string name_;
    double price_;

    // Знижка у відсотках
    double discount_;

public:
    // discount = 0 означає відсутність знижки
    Product(
        string name,
        double price,
        double discount = 0
    ) : name_(move(name)),
        price_(price),
        discount_(discount) {

        assert(price >= 0);
        assert(discount >= 0 && discount <= 100);
    }

    // Ціна після застосування знижки
    double final_price() const {
        return price_ * (1 - discount_ / 100);
    }

    // Встановлюємо нову знижку
    void set_discount(double p) {
        assert(p >= 0 && p <= 100);
        discount_ = p;
    }

    // Загальна ціна за кількість товарів
    double total(int qty) const {
        assert(qty >= 0);
        return final_price() * qty;
    }
};

void tests() {
    Product a("A", 100);

    // Без знижки
    assert(a.final_price() == 100);

    // Знижка 20%
    a.set_discount(20);

    assert(a.final_price() == 80);
    assert(a.total(3) == 240);

    // Знижка 100% = безкоштовно
    Product b("B", 50, 100);

    assert(b.final_price() == 0);
}

int main() {
    tests();

    // Незалежні товари
    Product a("Phone", 10000, 10);
    Product b("Mouse", 1000);
    Product c("Book", 500, 20);

    cout << a.final_price() << ' '
        << b.final_price() << '\n';

    c.set_discount(50);

    cout << c.total(2) << '\n';

    cout << "Tests passed\n";
}