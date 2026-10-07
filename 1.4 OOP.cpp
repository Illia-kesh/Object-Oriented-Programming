#include <cassert>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

/** Book stores bibliographic data and current reading progress. */
class Book {
    // Дані книги
    string title_;
    string author_;
    int pages_;

    // Скільки сторінок вже прочитано
    int current_;

public:
    // Створення книги
    Book(string title, string author, int pages)
        : title_(move(title)),
        author_(move(author)),
        pages_(pages),
        current_(0) {
        // Кількість сторінок не може бути від'ємною
        assert(pages >= 0);
    }

    // Читаємо n сторінок
    void read(int n) {
        assert(n >= 0);

        // Не можна прочитати більше сторінок,
        // ніж є в книзі
        current_ = min(pages_, current_ + n);
    }

    // Відсоток прочитаної книги
    double progress() const {
        return pages_ == 0
            ? 100.0
            : current_ * 100.0 / pages_;
    }

    // Перевірка, чи книга прочитана повністю
    bool is_finished() const {
        return current_ == pages_;
    }

    // Повертаємо автора
    const string& author() const {
        return author_;
    }

    // Повертаємо кількість сторінок
    int pages() const {
        return pages_;
    }
};

void tests() {
    Book a("A", "Author", 100);

    // Прочитано 30%
    a.read(30);
    assert(a.progress() == 30);
    assert(!a.is_finished());

    // Не можна вийти за межі книги
    a.read(100);
    assert(a.is_finished());

    // Граничний випадок: книга без сторінок
    Book b("B", "Author", 0);
    assert(b.is_finished());
    assert(b.progress() == 100);
}

int main() {
    tests();

    // Незалежні книги
    Book a("A", "One", 100);
    Book b("B", "Two", 50);
    Book c("C", "One", 200);

    a.read(25);
    b.read(50);

    cout << a.progress() << ' '
        << b.progress() << ' '
        << c.progress() << '\n';

    cout << "Tests passed\n";
}