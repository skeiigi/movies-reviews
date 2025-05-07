from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Movies, Reviews, Comment, Notification
from .forms import MovieForm, ReviewForm, LoginForm, RegisterForm, CommentForm


def index(request):
    return render(request, "moviesApp/index.html")


def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Передаем данные из POST-запроса в форму
        if form.is_valid():
            # Получаем данные из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Проверяем, существует ли пользователь с такими данными
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Если пользователь найден, выполняем вход
                login(request, user)
                return redirect('profile')  # Перенаправляем на главную страницу или другую страницу
            else:
                # Если пользователь не найден, выводим сообщение об ошибке
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            # Если форма не валидна, выводим сообщение об ошибке
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = LoginForm()  # Создаем пустую форму для GET-запроса

    return render(request, 'moviesApp/login.html', {'form': form})


def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "moviesApp/register.html", {"form": form})


def auth_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        return redirect('home')  # Перенаправляем на главную страницу
    else:
        # Если это не POST-запрос, просто перенаправляем на главную страницу
        return redirect('home')


@login_required(login_url='/login/')
def profile(request):
    user = get_object_or_404(User, username=request.user)
    return render(request, "moviesApp/profile.html", {"user": user})


def movies(request):
    # Получаем все фильмы из базы данных
    movies_list = Movies.objects.all()

    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user)
    else:
        user = None

    if request.method == "POST":
        # Если запрос POST, создаем форму с данными из запроса
        form = MovieForm(request.POST, request.FILES)  # Добавляем request.FILES для загрузки изображений
        if form.is_valid():
            # Если форма валидна, сохраняем данные и перенаправляем на страницу
            form.save()
            return render(request, "moviesApp/movies_page.html", {'form': form, 'movies': movies_list})
    else:
        # Если запрос GET, создаем пустую форму
        form = MovieForm()

    # Передаем форму и список фильмов в контекст
    return render(request, "moviesApp/movies_page.html", {'form': form, 'movies': movies_list, 'user': user})


@login_required(login_url='/login/')
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return HttpResponse(status=204)  # Успешно, без контента
    else:
        form = MovieForm(instance=movie)

    html = render_to_string('moviesApp/edit_movie_form.html', {'form': form}, request=request)
    return HttpResponse(html)


@login_required(login_url='/login/')
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    movie.delete()
    return redirect("movies")


def reviews(request):
    user = request.user if request.user.is_authenticated else None

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    mvs = Movies.objects.all()
    rvws = Reviews.objects.select_related('user', 'movie').all()
    return render(request, 'moviesApp/reviews_page.html', {'reviews': rvws, 'form': form, 'movies': mvs, "user": user})


@login_required(login_url='/login/')
def my_reviews(request):
    mvs = Movies.objects.all()
    rvws = Reviews.objects.filter(user=request.user).select_related('movie')
    user = request.user

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('my_reviews')
    else:
        form = ReviewForm()

    return render(request, 'moviesApp/my_reviews_page.html', {'reviews': rvws, 'movies': mvs, 'user': user, 'form': form})


@login_required(login_url='/login/')
def edit_review(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return HttpResponse(status=204)  # Успешно, без контента
    else:
        form = ReviewForm(instance=review)

    html = render_to_string('moviesApp/edit_review_form.html', {'form': form}, request=request)
    return HttpResponse(html)


@login_required(login_url='/login/')
def delete_review(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    review.delete()
    return redirect("my_reviews")


#Комментарии
def review_detail(request, review_id):
    print("💬 Вызвана review_detail()")  # Добавим это
    review = get_object_or_404(Reviews, id=review_id)
    comments = Comment.objects.filter(review=review, parent=None).select_related('user').prefetch_related('replies__user')
    form = CommentForm()

    return render(request, 'moviesApp/review_detail.html', {
        'review': review,
        'comments': comments,
        'form': form,
    })

@login_required
def add_comment(request, review_id, parent_id=None):
    review = get_object_or_404(Reviews, id=review_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.parent = parent
            comment.save()

            # Уведомление
            if parent and parent.user != request.user:
                Notification.objects.create(
                    recipient=parent.user,
                    comment=comment
                )

    return redirect('review_detail', review_id=review.id)