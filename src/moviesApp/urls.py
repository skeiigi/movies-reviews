from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('movies/', views.movies, name="movies"),
    path('reviews/', views.reviews, name="reviews"),
    path('profile/', views.profile, name="profile"),
    path('login/', views.auth_login, name="login"),
    path('register/', views.auth_register, name="register"),
    path('logout/', views.auth_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)