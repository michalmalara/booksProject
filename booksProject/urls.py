from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


import books.urls as books_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(books_urls)),
    
    path(r'login/', auth_views.LoginView.as_view(), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
