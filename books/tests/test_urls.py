from django.test import SimpleTestCase
from django.urls import resolve, reverse

from books.views import BooksListView


class TestUrls(SimpleTestCase):
    def test_books_list_url_ok(self):
        url = reverse('books-list')
        self.assertEquals(resolve(url).func.__name__, BooksListView.as_view().__name__)
        self.assertTemplateUsed('book_list.html')
