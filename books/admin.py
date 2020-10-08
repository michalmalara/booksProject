from django.contrib import admin
from .models import Book
# Register your models here.


class BookAdminView(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'pub_date', 'isbn', 'pages', 'cover', 'lang']
    search_fields = ['title', 'author', 'pub_date', 'isbn']
    readonly_fields = []

    filter_horizontal = []
    list_filter = ['lang', ]
    fieldsets = []

admin.site.register(Book, BookAdminView)