from django.contrib import admin
from django.urls import path, include

from books import views

import books.urls as books_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(books_urls))
]
