import rest_framework
from rest_framework import viewsets, permissions

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .serializers import BookSerializer
from ..models import Book


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BooksViewSet(viewsets.ModelViewSet):
    """
        Protected viewset for reading, creating, updating and deleting objects in Books table. Only for logged in users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    search_fields = ['title', 'author', 'isbn', 'lang', 'pub_date']
    filterset_fields = ['lang', 'author', 'pub_date']
    ordering_fields = ['title', 'author', 'isbn', 'lang', 'pub_date']


class BooksPublicViewSet(viewsets.ModelViewSet):
    """
        Viewset for reading objects in Books table.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'author', 'isbn', 'lang', 'pub_date']
    filterset_fields = ['lang', 'author', 'pub_date']
    ordering_fields = ['title', 'author', 'isbn', 'lang', 'pub_date']
    http_method_names = ['get', 'options']