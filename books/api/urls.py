from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from books.api.views import BooksViewSet, BooksPublicViewSet

router = routers.DefaultRouter()
router.register(r'auth/books', BooksViewSet, basename='books-api-view')
router.register('books', BooksPublicViewSet, basename='books-public-api-view')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api-login'),
    path('api_auth/', include('rest_framework.urls'), name='api-auth'),
]
