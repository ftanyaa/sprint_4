import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# ---------- add_new_book ----------

def test_add_new_book_adds_book(collector):
    collector.add_new_book('Гарри Поттер')
    assert 'Гарри Поттер' in collector.books_genre


def test_add_new_book_has_empty_genre(collector):
    collector.add_new_book('Винни-Пух')
    assert collector.books_genre['Винни-Пух'] == ''


@pytest.mark.parametrize(
    'name, expected',
    [
        ('A', True),
        ('A' * 40, True),
        ('A' * 41, False),
    ]
)
def test_add_new_book_name_length(collector, name, expected):
    collector.add_new_book(name)
    assert (name in collector.books_genre) == expected


# ---------- set_book_genre / get_book_genre ----------

def test_set_book_genre_sets_valid_genre(collector):
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Фантастика')
    assert collector.get_book_genre('1984') == 'Фантастика'


def test_set_book_genre_invalid_genre_not_set(collector):
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Роман')
    assert collector.get_book_genre('1984') == ''


# ---------- get_books_with_specific_genre / get_books_genre ----------

def test_get_books_with_specific_genre_returns_correct_books(collector):
    collector.add_new_book('Оно')
    collector.add_new_book('Назад в будущее')
    collector.set_book_genre('Оно', 'Ужасы')
    collector.set_book_genre('Назад в будущее', 'Фантастика')

    result = collector.get_books_with_specific_genre('Фантастика')

    assert result == ['Назад в будущее']


def test_get_books_genre_returns_books_dict(collector):
    collector.add_new_book('Книга')
    assert collector.get_books_genre() == {'Книга': ''}


# ---------- get_books_for_children ----------

def test_get_books_for_children_excludes_age_rating_genres(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')

    collector.add_new_book('Карлсон')
    collector.set_book_genre('Карлсон', 'Мультфильмы')

    result = collector.get_books_for_children()

    assert 'Карлсон' in result
    assert 'Оно' not in result


# ---------- favorites ----------

def test_add_book_in_favorites_adds_book(collector):
    collector.add_new_book('Шрек')
    collector.add_book_in_favorites('Шрек')

    assert 'Шрек' in collector.get_list_of_favorites_books()


def test_add_book_in_favorites_not_added_twice(collector):
    collector.add_new_book('Шрек')
    collector.add_book_in_favorites('Шрек')
    collector.add_book_in_favorites('Шрек')

    assert collector.get_list_of_favorites_books().count('Шрек') == 1


def test_delete_book_from_favorites_removes_book(collector):
    collector.add_new_book('Шрек')
    collector.add_book_in_favorites('Шрек')
    collector.delete_book_from_favorites('Шрек')

    assert 'Шрек' not in collector.get_list_of_favorites_books()
