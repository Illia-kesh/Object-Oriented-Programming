"""Task 2.6: Ticket with automatic unique ids."""


class Ticket:
    """A ticket with an automatically assigned unique, increasing ``id``."""

    _created = 0

    def __init__(self):
        """Create a ticket and assign it the next id."""
        Ticket._created += 1
        self.id = Ticket._created

    @classmethod
    def created(cls):
        """Return the number of tickets created."""
        return cls._created


def demo():
    tk1, tk2, tk3 = Ticket(), Ticket(), Ticket()
    print("id:", tk1.id, tk2.id, tk3.id, "| created:", Ticket.created())


# ------------------------------- tests ------------------------------------
def test_ticket_ids_unique_and_increasing():
    a, b, c = Ticket(), Ticket(), Ticket()
    assert a.id < b.id < c.id
    assert len({a.id, b.id, c.id}) == 3


def test_ticket_created_counts():
    before = Ticket.created()
    Ticket()
    Ticket()
    assert Ticket.created() == before + 2


def test_ticket_ids_consecutive():
    a, b = Ticket(), Ticket()
    assert b.id == a.id + 1


if __name__ == "__main__":
    demo()