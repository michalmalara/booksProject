from django.shortcuts import render
from django.views.generic import ListView
from django.template.defaulttags import register

from .models import Book


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
