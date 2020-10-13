from django.urls import path
from django.conf.urls.static import static

from books import views

urlpatterns = [
    path('', views.BooksListView.as_view(), name='books-list'),
    path('import/', views.import_book, name='import-books'),
    path('add_book', views.BookCreateView.as_view(), name='book-create'),
    path('edit_book/<int:pk>', views.BookEditView.as_view(), name='book-edit'),
    path('delete_book/<int:pk>', views.BookDeleteView.as_view(), name='book-delete'),
]

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)