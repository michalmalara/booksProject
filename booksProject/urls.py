from django.contrib import admin
from django.urls import path, include

import books.urls as books_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(books_urls))
]
