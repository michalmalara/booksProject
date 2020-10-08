from datetime import datetime

from django.test import TestCase

from books.models import Book


class TestBooks(TestCase):
    def setUp(self) -> None:
        self.book = Book()
        self.book.title = 'tytul 1'
        self.book.author = 'autor 1'
        self.book.isbn = 123456789
        self.book.pages = 45
        self.book.pub_date = datetime.now()
        self.book.cover = 'https://www.google.com/'
        self.book.save()

    def test_book_created(self):
        queryset = Book.objects.all()

        print((queryset[0]))

        self.assertEquals(len(queryset), 1)

    def test_book_str_ok(self):
        queryset = Book.objects.all()

        print((queryset[0]))

        self.assertEquals(queryset[0].__str__(), f'{self.book.title} - {self.book.author}')
