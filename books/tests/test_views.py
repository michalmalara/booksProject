import random
from datetime import datetime, date

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from books.models import Book
from books.views import param_replace


class TestParamReplace(TestCase):
    def test_param_replace(self):
        factory = RequestFactory()
        request = factory.get('/?sort_by=title&ascending=true')
        context = {'request': request}
        func_resp = param_replace(context)

        self.assertEquals(func_resp, 'sort_by=title&ascending=true')


class TestBooksListView(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user1 = User.objects.create_user(username='testuser1', password='abcd')
        self.test_user1.save()

        self.books = []

        for i in range(1, 30):
            book = Book()
            book.title = f'tytul {i}'
            book.author = f'autor {i}'
            book.isbn = random.randint(1000000000000, 9999999999999)
            book.pages = random.randint(10, 999)
            book.pub_date = date(year=2020, month=random.randint(3, 12), day=i)
            book.cover = 'https://www.google.com/'
            if i < 15:
                book.lang = 'PL'
            else:
                book.lang = 'EN'
            book.save()

            self.books.append(book)

    def test_books_list_view(self):
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_books_list_view_pagination(self):
        url = reverse('books-list')
        self.client.login(username='testuser1', password='abcd')

        response = self.client.get(url)
        for i in range(1,10):
            self.assertContains(response, f'tytul {i}')
        self.assertNotContains(response, f'tytul {i+2}')

        response = self.client.get(url + '?page=2')
        self.assertNotContains(response, f'tytul 10')
        for i in range(11, 21):
            self.assertContains(response, f'tytul {i}')
        self.assertNotContains(response, f'tytul {i+1}')


    def test_books_list_view_searching(self):
        url = reverse('books-list')
        self.client.login(username='testuser1', password='abcd')

        response = self.client.get(url + f'?title={self.books[5].title}')
        self.assertContains(response, self.books[5].title)

        response = self.client.get(url + f'?author={self.books[24].author}')
        self.assertContains(response, self.books[24].title)

        response = self.client.get(url + f'?isbn={self.books[14].isbn}')
        self.assertContains(response, self.books[14].title)

        response = self.client.get(url + f'?lang={self.books[5].lang}')
        self.assertContains(response, self.books[5].title)

        response = self.client.get(url + '?sorting=title&sorting_direction=ASC')
        self.assertContains(response, self.books[0].title)

        response = self.client.get(url + '?sorting=title&sorting_direction=DESC')
        self.assertContains(response, self.books[-1].title)
