from django.test import SimpleTestCase
from django.urls import resolve, reverse

from books.views import BooksListView, BookCreateView, BookDeleteView, BookEditView


class TestUrls(SimpleTestCase):
    def test_books_list_url_ok(self):
        url = reverse('books-list')
        self.assertEquals(resolve(url).func.__name__, BooksListView.as_view().__name__)
        self.assertTemplateUsed('book_list.html')

    def test_books_create_url_ok(self):
        url = reverse('book-create')
        self.assertEquals(resolve(url).func.__name__, BookCreateView.as_view().__name__)
        self.assertTemplateUsed('book_form.html')

    def test_books_edit_url_ok(self):
        url = reverse('book-edit', args=[0])
        self.assertEquals(resolve(url).func.__name__, BookEditView.as_view().__name__)
        self.assertTemplateUsed('book_form.html')

    def test_books_delete_url_ok(self):
        url = reverse('book-delete', args=[0])
        self.assertEquals(resolve(url).func.__name__, BookDeleteView.as_view().__name__)
        self.assertTemplateUsed('book_delete_confirmation.html')