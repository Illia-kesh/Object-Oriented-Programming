#include <algorithm>
#include <cassert>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;

/** Student stores a surname and a list of grades. */
class Student {
    // Прізвище студента
    string surname_;

    // Список оцінок
    vector<int> grades_;

public:
    // Створення студента
    Student(string surname)
        : surname_(move(surname)) {
    }

    // Додаємо оцінку
    void add_grade(int grade) {
        // Оцінка повинна бути від 0 до 100
        assert(grade >= 0 && grade <= 100);
        grades_.push_back(grade);
    }

    // Середнє арифметичне оцінок
    double average() const {
        if (grades_.empty())
            return 0;

        return static_cast<double>(
            accumulate(
                grades_.begin(), grades_.end(), 0
            )
            ) / grades_.size();
    }

    // Найкраща оцінка
    int best() const {
        if (grades_.empty())
            return 0;

        return *max_element(
            grades_.begin(), grades_.end()
        );
    }

    // Чи є оцінка нижче 60
    bool has_debt() const {
        return any_of(
            grades_.begin(),
            grades_.end(),
            [](int g) {
                return g < 60;
            }
        );
    }
};

void tests() {
    Student a("A");

    // Порожній список оцінок
    assert(a.average() == 0);
    assert(a.best() == 0);
    assert(!a.has_debt());

    // Студент має незадовільну оцінку
    a.add_grade(80);
    a.add_grade(40);

    assert(a.has_debt());
    assert(a.best() == 80);

    // 60 — це вже не борг
    Student b("B");
    b.add_grade(60);

    assert(!b.has_debt());
}

int main() {
    tests();

    // Три незалежні студенти
    Student a("Ivan");
    Student b("Oleh");
    Student c("Anna");

    a.add_grade(90);
    a.add_grade(80);

    b.add_grade(55);
    c.add_grade(100);

    cout << a.average() << ' '
        << b.has_debt() << '\n';

    cout << c.best() << '\n';
    cout << "Tests passed\n";
}