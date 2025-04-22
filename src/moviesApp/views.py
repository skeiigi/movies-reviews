from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Movies, Reviews
from .forms import MovieForm, ReviewForm, LoginForm, RegisterForm


def index(request):
    return render(request, "index.html")


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
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect('profile')  # Перенаправляем на главную страницу или другую страницу
            else:
                # Если пользователь не найден, выводим сообщение об ошибке
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            # Если форма не валидна, выводим сообщение об ошибке
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = LoginForm()  # Создаем пустую форму для GET-запроса

    return render(request, 'login.html', {'form': form})


def auth_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def auth_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Вы успешно вышли из системы.")
        return redirect('home')  # Перенаправляем на главную страницу
    else:
        # Если это не POST-запрос, просто перенаправляем на главную страницу
        return redirect('home')


@login_required(login_url='/login/')
def profile(request):
    user = get_object_or_404(User, username=request.user)
    return render(request, "profile.html", {"user": user})


def movies(request):
    # Получаем все фильмы из базы данных
    movies_list = Movies.objects.all

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
            return render(request, "movies_page.html", {'form': form, 'movies': movies_list})
    else:
        # Если запрос GET, создаем пустую форму
        form = MovieForm()

    # Передаем форму и список фильмов в контекст
    return render(request, "movies_page.html", {'form': form, 'movies': movies_list, 'user': user})


def reviews(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user)
    else:
        user = None

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    mvs = Movies.objects.all()
    rvws = Reviews.objects.all()
    return render(request, 'reviews_page.html', {'reviews': rvws, 'form': form, 'movies': mvs, "user": user})