import json
import requests

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.defaulttags import register

from .models import Book
from .forms import BooksSearchForm, ImportBooksForm


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Function returns GET parameters to use with pagination next/prev data.
    It allows to keep search and ordering settings after changing pages or sorting.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


class BooksListView(ListView):
    model = Book
    ordering = 'pk'
    paginate_by = 10
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        search_form = BooksSearchForm(self.request.GET)

        if search_form.is_valid():
            title = search_form.cleaned_data.get('title', '').strip()
            if title:
                queryset = queryset.filter(title__icontains=title)
            author = search_form.cleaned_data.get('author', '').strip()
            if author:
                queryset = queryset.filter(author__icontains=author)
            isbn = search_form.cleaned_data.get('isbn', '')
            if isbn:
                queryset = queryset.filter(isbn=isbn)
            lang = search_form.cleaned_data.get('lang', '').strip()
            if lang:
                queryset = queryset.filter(lang=lang.upper())

            published_starting_date = search_form.cleaned_data['published_starting_date']
            published_ending_date = search_form.cleaned_data['published_ending_date']
            if published_starting_date and published_ending_date:
                queryset = queryset.filter(pub_date__gte=published_ending_date,
                                           pub_date__lte=published_ending_date)
            if published_starting_date and not published_ending_date:
                queryset = queryset.filter(pub_date__gte=published_starting_date)
            if not published_starting_date and published_ending_date:
                queryset = queryset.filter(pub_date__lte=published_ending_date)

        sort_dir = {
            'title': 'asc',
            'author': 'asc',
            'pub_date': 'asc',
            'pages': 'asc',
            'isbn': 'asc',
            'lang': 'asc',
        }

        if 'sorting' in self.request.GET:
            sorting = self.request.GET['sorting']

            if 'sort_dir' in self.request.GET:
                sort_dir_ = self.request.GET['sort_dir']
                if sorting in sort_dir:
                    if sort_dir_ == 'asc':
                        sort_dir[sorting] = 'desc'
                    else:
                        sort_dir[sorting] = 'asc'
                        sorting = '-' + sorting

            queryset = queryset.order_by(sorting, '-pk')

        return super().get_context_data(
            search_form=search_form,
            object_list=queryset,
            sort_dir=sort_dir,
            **kwargs)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = '/'


class BookEditView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    success_url = '/'


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/'


def import_book(request):
    form = ImportBooksForm()

    if request.method == 'POST':
        api_url = 'https://www.googleapis.com/books/v1/volumes'
        api_data = {
            'q': request.POST['intitle'],
            'inauthor': request.POST['inauthor'],
            'inpublisher': request.POST['inpublisher'],
            'subject': request.POST['subject'],
            'isbn': request.POST['isbn'],
            'lccn': request.POST['lccn'],
            'oclc': request.POST['oclc'],
            'maxResults': request.POST['positions_count']
        }

        response = requests.get(api_url, api_data)
        if response.status_code == 200:
            response_data = response.json()
            info = []
            errors = 0
            for i, b in enumerate(response_data['items']):
                book = Book()

                try:
                    book.title = b['volumeInfo']['title']
                    book.author = ', '.join(b['volumeInfo']['authors'])

                    if len(b['volumeInfo']['publishedDate']) == 4:
                        pub_date_ = b['volumeInfo']['publishedDate'] + '-01-01'
                    elif len(b['volumeInfo']['publishedDate']) == 7:
                        pub_date_ = b['volumeInfo']['publishedDate'] + '-01'
                    else:
                        pub_date_ = b['volumeInfo']['publishedDate']
                    book.pub_date = pub_date_

                    book.isbn = b['volumeInfo']['industryIdentifiers'][0]['identifier']

                    book.pages = b['volumeInfo']['pageCount']

                    if 'imageLinks' in b['volumeInfo']:
                        book.cover = b['volumeInfo']['imageLinks']['thumbnail']

                    book.lang = b['volumeInfo']['language']

                    book.save()
                except KeyError as e:
                    info.append(f'Błąd przy dodawaniu książki "{b["volumeInfo"]["title"]}". Brak pola {e}')
                    errors += 1

                except Exception as e:
                    info.append(f'Błąd przy dodawaniu książki {b["volumeInfo"]["title"]}')
                    errors += 1

            return render(request, 'books/import_books.html',
                          {'form': form, 'info': info, 'succes_info': f'Dodano książek: {i + 1 - errors} z {i+1}.'})

        elif response.status_code == 400:
            return render(request, 'books/import_books.html',
                          {'form': form, 'info': ['Nie znaleziono tej książki.']})
        else:
            return render(request, 'books/import_books.html',
                          {'form': form, 'info': [f'Błąd zewnętrznego serwera! (Kod: {response.status_code})']})

    return render(request, 'books/import_books.html',
                  {'form': form, 'info': []})
