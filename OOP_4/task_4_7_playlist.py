"""Задача 4.7 — клас Playlist."""
import pytest


def _check_song(song):
    if not isinstance(song, str) or not song.strip():
        raise ValueError("назва пісні має бути непорожнім рядком")


class Playlist:
    def __init__(self, *songs):
        for s in songs:
            _check_song(s)
        self._songs = list(songs)

    def __str__(self):
        return "Playlist: " + ", ".join(self._songs) if self._songs else "Playlist: (порожній)"

    def __repr__(self):
        return f"Playlist({', '.join(repr(s) for s in self._songs)})"

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return Playlist(*self._songs[i])
        return self._songs[i]

    def __contains__(self, song):
        return song in self._songs

    def __iter__(self):
        return iter(self._songs)

    def __bool__(self):
        return bool(self._songs)

    def __add__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented
        return Playlist(*self._songs, *other._songs)

    def __iadd__(self, song):
        """pl += "назва" — додає пісню (змінює плейлист на місці)."""
        if not isinstance(song, str):
            return NotImplemented  # для Playlist спрацює __add__
        _check_song(song)
        self._songs.append(song)
        return self

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented
        return self._songs == other._songs

    __hash__ = None  # плейлист змінюваний


# ---------------------------- тести ----------------------------

def test_container_basics():
    pl = Playlist("A", "B", "C")
    assert len(pl) == 3
    assert pl[0] == "A" and pl[-1] == "C"
    assert "B" in pl and "Z" not in pl
    assert list(pl) == ["A", "B", "C"]
    assert [s for s in pl] == ["A", "B", "C"]


def test_slices():
    pl = Playlist("A", "B", "C", "D")
    assert pl[1:3] == Playlist("B", "C")
    assert pl[::-1] == Playlist("D", "C", "B", "A")
    assert pl[10:] == Playlist()
    assert isinstance(pl[:2], Playlist)
    with pytest.raises(IndexError):
        pl[10]


def test_bool():
    assert not Playlist()
    assert Playlist("A")
    assert bool(Playlist()) is False


def test_add_returns_new():
    a, b = Playlist("A"), Playlist("B", "C")
    c = a + b
    assert c == Playlist("A", "B", "C")
    assert a == Playlist("A") and b == Playlist("B", "C")  # не змінились
    assert c is not a


def test_iadd_appends_song():
    pl = Playlist("A")
    same = pl
    pl += "B"
    assert pl == Playlist("A", "B")
    assert pl is same
    pl += Playlist("C", "D")  # через __add__
    assert list(pl) == ["A", "B", "C", "D"]


def test_str_repr():
    pl = Playlist("A", "B")
    assert str(pl) == "Playlist: A, B"
    assert str(Playlist()) == "Playlist: (порожній)"
    assert repr(pl) == "Playlist('A', 'B')"
    assert eval(repr(pl)) == pl


@pytest.mark.parametrize("songs", [("A", ""), ("A", 5), (None,), ("  ",)])
def test_invalid_init(songs):
    with pytest.raises(ValueError):
        Playlist(*songs)


def test_invalid_iadd_empty_song():
    pl = Playlist("A")
    with pytest.raises(ValueError):
        pl += ""
    assert len(pl) == 1


def test_incompatible_types():
    pl = Playlist("A")
    with pytest.raises(TypeError):
        pl + "B"
    with pytest.raises(TypeError):
        pl + 5
    with pytest.raises(TypeError):
        pl += 5
    assert (pl == ["A"]) is False
