from django.conf.urls import url
from django.urls import path, include

from rest_framework import routers, permissions
from rest_framework.authtoken.views import obtain_auth_token

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from books.api.views import BooksViewSet

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Books API",
#         default_version='v1',
#         description="API for Books application",
#         contact=openapi.Contact(email="michalmalara@gmail.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet, basename='books-api-view')

urlpatterns = [
    path(r'', include(router.urls)),
    path('login/', obtain_auth_token, name='api-login'),
    path('api-auth/', include('rest_framework.urls')),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema_json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
]
