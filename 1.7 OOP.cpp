#include <cassert>
#include <iostream>
#include <optional>
#include <vector>
using namespace std;

/** Stack stores integers using last-in, first-out order. */
class Stack {
    // vector використовується як сховище стека
    vector<int> data_;

public:
    // Додаємо елемент на вершину
    void push(int x) {
        data_.push_back(x);
    }

    // Видаляємо верхній елемент
    optional<int> pop() {
        // Порожній стек не має елемента
        if (data_.empty())
            return nullopt;

        int value = data_.back();
        data_.pop_back();

        return value;
    }

    // Дивимося верхній елемент без видалення
    optional<int> peek() const {
        if (data_.empty())
            return nullopt;

        return data_.back();
    }

    // Кількість елементів
    size_t size() const {
        return data_.size();
    }

    // Перевірка на порожність
    bool is_empty() const {
        return data_.empty();
    }
};

void tests() {
    Stack a;

    // Порожній стек
    assert(a.is_empty());
    assert(a.size() == 0);

    // Аналог None
    assert(!a.pop().has_value());
    assert(!a.peek().has_value());

    // Перевірка принципу LIFO
    a.push(10);
    a.push(20);

    assert(a.peek() == 20);
    assert(a.pop() == 20);
    assert(a.size() == 1);
}

int main() {
    tests();

    // Незалежні стеки
    Stack a;
    Stack b;
    Stack c;

    a.push(1);
    a.push(2);
    b.push(7);

    cout << a.pop().value()
        << ' ' << a.size() << '\n';

    cout << b.peek().value()
        << ' ' << c.is_empty() << '\n';

    cout << "Tests passed\n";
}