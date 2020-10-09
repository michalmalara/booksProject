from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.defaulttags import register

from .models import Book
from .forms import BooksSearchForm


# Create your views here.

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Function returns GET parameters to use with pagination next/prev data.
    It allows to keep search and ordering settings with pagination.
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

            sorting = search_form.cleaned_data['sorting']
            if sorting:
                sorting_direction = search_form.cleaned_data['sorting_direction']
                if sorting_direction == 'DESC':
                    sorting = '-' + sorting
                queryset = queryset.order_by(sorting, '-pk')

            published_starting_date = search_form.cleaned_data['published_starting_date']
            published_ending_date = search_form.cleaned_data['published_ending_date']
            if published_starting_date and published_ending_date:
                queryset = queryset.filter(created__gte=published_ending_date,
                                           created__lte=published_ending_date)
            if published_starting_date and not published_ending_date:
                queryset = queryset.filter(created__gte=published_starting_date)
            if not published_starting_date and published_ending_date:
                queryset = queryset.filter(created__lte=published_ending_date)

        return super().get_context_data(
            search_form=search_form,
            object_list=queryset,
            **kwargs)


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    success_url = '/'


class BookEditView(UpdateView):
    model = Book
    fields = '__all__'
    success_url = '/'


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/'
