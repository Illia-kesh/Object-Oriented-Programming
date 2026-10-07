#include <cassert>
#include <cmath>
#include <iostream>
using namespace std;

/** Point represents a point on a two-dimensional plane. */
class Point {
    // Координати точки
    double x_, y_;

public:
    // Конструктор задає початкові координати
    Point(double x, double y) : x_(x), y_(y) {}

    // Обчислюємо відстань між двома точками
    double distance_to(const Point& other) const {
        return std::hypot(x_ - other.x_, y_ - other.y_);
    }

    // Зсуваємо точку на dx та dy
    void move(double dx, double dy) {
        x_ += dx;
        y_ += dy;
    }

    // Перевіряємо, чи точка знаходиться в (0, 0)
    bool is_origin() const {
        return x_ == 0 && y_ == 0;
    }
};

void tests() {
    // Звичайний випадок: відстань 3-4-5
    Point a(0, 0), b(3, 4);
    assert(a.distance_to(b) == 5);

    // Перевіряємо переміщення
    a.move(2, 3);
    assert(!a.is_origin());

    // Граничний випадок: початок координат
    Point c(0, 0);
    assert(c.is_origin());
}

int main() {
    tests();

    // Створюємо незалежні об'єкти
    Point a(1, 2);
    Point b(5, 6);
    Point c(0, 0);

    a.move(2, -1);

    cout << a.distance_to(b) << '\n';
    cout << b.is_origin() << ' '
        << c.is_origin() << '\n';

    cout << "Tests passed\n";
}