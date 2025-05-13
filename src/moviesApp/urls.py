from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

    # --ГЛАВНЫЕ СТРАНИЦЫ--
    path('', views.index, name="home"),
    path('profile/', views.profile_view, name="profile"),

    # --АККАУНТ ПОЛЬЗОВАТЕЛЯ--
    path('login/', views.auth_login, name="login"),
    path('register/', views.auth_register, name="register"),
    path('logout/', views.auth_logout, name='logout'),
    path('user/<int:user_id>/', views.profile_view, name="user_profile"),

    # --ОБСУЖДЕНИЯ--
    path('reviews/', views.reviews, name="reviews"),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path("my_reviews/delete/<int:review_id>/", views.delete_review, name="delete_review"),

    # --ФИЛЬМЫ--
    path('admin.movies/', views.movies_admin, name="admin_movies"),
    path('movies/', views.movies_user, name="movies"),
    path('movie/<int:movie_id>', views.movie_page, name='movie'),
    path('movie/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path("movie/delete/<int:movie_id>/", views.delete_movie, name="delete_movie"),

    # --КОММЕНТАРИИ--
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/<int:review_id>/comment/', views.add_comment, name='add_comment'),
    path('review/<int:review_id>/reply/<int:parent_id>/', views.add_comment, name='reply_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)