#include <cassert>
#include <iostream>
using namespace std;

/** Rectangle stores width and height and calculates its geometry. */
class Rectangle {
    // Розміри прямокутника
    double width_, height_;

public:
    // Конструктор задає ширину та висоту
    Rectangle(double width, double height)
        : width_(width), height_(height) {
        // Розміри не можуть бути від'ємними
        assert(width >= 0 && height >= 0);
    }

    // Формула площі: ширина * висота
    double area() const {
        return width_ * height_;
    }

    // Формула периметра
    double perimeter() const {
        return 2 * (width_ + height_);
    }

    // Квадрат має однакову ширину та висоту
    bool is_square() const {
        return width_ == height_;
    }
};

void tests() {
    // Перевірка площі та периметра
    Rectangle a(3, 4);
    assert(a.area() == 12);
    assert(a.perimeter() == 14);

    // Перевірка квадрата
    Rectangle b(5, 5);
    assert(b.is_square());

    // Граничний випадок: нульова ширина
    Rectangle c(0, 7);
    assert(c.area() == 0);
}

int main() {
    tests();

    // Три незалежні прямокутники
    Rectangle a(3, 4);
    Rectangle b(5, 5);
    Rectangle c(2, 6);

    cout << a.area() << ' '
        << a.perimeter() << '\n';

    cout << b.is_square() << ' '
        << c.is_square() << '\n';

    cout << "Tests passed\n";
}