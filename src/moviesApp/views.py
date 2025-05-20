from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.views.decorators.http import require_POST


from .models import Movies, Reviews, Comment, Notification, MovieComment
from .forms import MovieForm, ReviewForm, LoginForm, RegisterForm, CommentForm, MovieCommentForm


# ВСПОМОГАТЕЛЬНЫЙ МЕТОД ДЛЯ СКРЫТИЯ СТРАНИЦЫ С АДМИНКОЙ
def is_admin(user):
    return user.is_superuser


# ------------------------ГЛАВНЫЕ СТРАНИЦЫ------------------------

# ГЛАВНАЯ СТРАНИЦА
def index(request):
    return render(request, "moviesApp/index.html")


# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
def profile_view(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)

    review_count = Reviews.objects.filter(user=user, removed=False).count()
    comment_count = Comment.objects.filter(user=user, removed=False).count()

    return render(request, "moviesApp/profile.html",
                  {"user": user,
                   "review_count": review_count,
                   "comment_count": comment_count}
                  )


# ------------------------АККАУНТ ПОЛЬЗОВАТЕЛЯ------------------------

# АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
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


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
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


# ВЫХОД ИЗ АККАУНТА ПОЛЬЗОВАТЕЛЯ
def auth_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        return redirect('home')  # Перенаправляем на главную страницу
    else:
        # Если это не POST-запрос, просто перенаправляем на главную страницу
        return redirect('home')


# ------------------------ФИЛЬМЫ------------------------

# СТРАНИЦА С ТАБЛИЦЕЙ ФИЛЬМОВ ДЛЯ АДМИНОВ
@user_passes_test(is_admin, login_url='movies')
def movies_admin(request):
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
            return render(request, "moviesApp/movies_admin.html", {'form': form, 'movies': movies_list})
    else:
        # Если запрос GET, создаем пустую форму
        form = MovieForm()

    # Передаем форму и список фильмов в контекст
    return render(request, "moviesApp/movies_admin.html", {'form': form, 'movies': movies_list, 'user': user})


# РЕДАКТИРОВАНИЕ ФИЛЬМОВ
@login_required(login_url='/login/')
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return HttpResponse(status=204)  # Успешно, без контента
    else:
        form = MovieForm(instance=movie)

    html = render_to_string('moviesApp/edit_movie_form.html', {'form': form}, request=request)
    return HttpResponse(html)


# УДАЛЕНИЕ ФИЛЬМОВ
@login_required(login_url='/login/')
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    movie.removed = True
    movie.save()
    return redirect("movies")


# СПИСОК ФИЛЬМОВ
def movies_user(request):
    movies_list = Movies.objects.filter(removed=False)

    return render(request, "moviesApp/movies_page.html", {"movies": movies_list})


# СТРАНИЦА ОПРЕДЕЛЕННОГО ФИЛЬМА
def movie_page(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    comments = MovieComment.objects.filter(movie=movie, removed=False).select_related('user')
    form = MovieCommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = MovieCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            return redirect('movie_page', movie_id=movie.id)
        
    return render(request, "moviesApp/movie.html", {
        "movie": movie,
        "comments": comments,
        "form": form,
    })

@login_required
@require_POST
def delete_movie_comment(request, comment_id):
    comment = get_object_or_404(MovieComment, id=comment_id, user=request.user)
    comment.removed = True
    comment.save()
    return JsonResponse({'success': True})


# Редактирование комментария
@login_required
def edit_movie_comment(request, comment_id):
    comment = get_object_or_404(MovieComment, id=comment_id, user=request.user)

    if request.method == 'POST':
        form = MovieCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'new_content': comment.content
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # GET-запрос — возвращаем форму
    form = MovieCommentForm(instance=comment)
    html = render_to_string('moviesApp/edit_movie_comment_form.html', {'form': form, 'comment': comment}, request=request)
    return JsonResponse({'html': html})


# ------------------------ОБСУЖДЕНИЯ------------------------

# СТРАНИЦА СО ВСЕМИ ОБСУЖДЕНИЯМИ
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
    mvs = Movies.objects.filter(removed=False)
    rvws = Reviews.objects.select_related('user', 'movie').filter(removed=False)
    return render(request, 'moviesApp/reviews_page.html', {'reviews': rvws, 'form': form, 'movies': mvs, "user": user})


# СТРАНИЦА С ОБСУЖДЕНИЯМИ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ
@login_required(login_url='/login/')
def my_reviews(request):
    mvs = Movies.objects.filter(removed=False)
    rvws = Reviews.objects.filter(user=request.user, removed=False).select_related('movie')
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

    return render(request, 'moviesApp/my_reviews_page.html',
                  {'reviews': rvws, 'movies': mvs, 'user': user, 'form': form})


# РЕДАКТИРОВАНИЕ ОБСУЖДЕНИЙ
@login_required(login_url='/login/')
def edit_review(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            if form.has_changed():
                form.save()
                # Возвращаем JSON с обновлёнными данными
                return JsonResponse({
                    'success': True,
                    'review': {
                        'id': review.id,
                        'title': review.title,
                        'content': review.content,
                        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
                        'changed_at': review.changed_at.strftime('%Y-%m-%d %H:%M') if review.changed_at else '',
                        'movie_title': review.movie.title if review.movie else '(Фильм не указан)',
                        'poster_url': review.movie.poster.url if review.movie and hasattr(review.movie.poster, 'url') else '',
                    }
                })
            else:
                return JsonResponse({'success': True, 'message': 'Изменений не было'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        # GET-запрос: возвращаем HTML-форму для модального окна
        form = ReviewForm(instance=review)
        html = render_to_string('moviesApp/edit_review_form.html', {'form': form}, request=request)
        return HttpResponse(html)


# УДАЛЕНИЕ ОБСУЖДЕНИЙ
@login_required(login_url='/login/')
def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Reviews.objects.get(id=review_id, user=request.user)
            review.removed = True
            review.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Статья успешно удалена'
                })

            # Если обычный запрос — редиректим
            return JsonResponse({
                'success': True,
                'redirect': request.META.get('HTTP_REFERER', '/')
            })

        except Reviews.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Статья не найдена'
                }, status=404)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Метод не поддерживается'
        }, status=405)

    return JsonResponse({
        'success': False,
        'error': 'Запрос не поддерживается'
    }, status=400)


# ------------------------КОММЕНТАРИИ------------------------

# СТРАНИЦА С КОММЕНТАРИЯМИ ОПРЕДЕЛЕННОГО ОБСУЖДЕНИЯ
def review_detail(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    comments = Comment.objects.filter(review=review, parent=None).select_related('user').prefetch_related(
        Prefetch(
            'replies',
            queryset=Comment.objects.filter(removed=False).select_related('user'),
            to_attr='filtered_replies'
        )
    )
    form = CommentForm()

    return render(request, 'moviesApp/review_detail.html', {
        'review': review,
        'comments': comments,
        'form': form,
    })


# ДОБАВЛЕНИЕ КОММЕНТАРИЕВ
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

            if parent is None and review.user != request.user:
                Notification.objects.create(
                    recipient = review.user,
                    comment=comment
                )

            # Уведомление об ответе на комментарий
            elif parent is not None and parent.user != request.user:
                Notification.objects.create(
                    recipient=parent.user,
                    comment=comment
                )

    return redirect('review_detail', review_id=review.id)


# ОТВЕТЫ НА КОММЕНТАРИИ
def reply_comment(request, pk, parent_id):
    review = get_object_or_404(Reviews, pk=pk)
    parent = get_object_or_404(Comment, pk=parent_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.parent = parent
            reply.save()

    return redirect('review_detail', pk=pk)


# УДАЛЕНИЕ КОММЕНТАРИЕВ/ОТВЕТОВ
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    review = comment.review
    comment.removed = True
    comment.save()
    messages.success(request, "Комментарий удалён.")
    return redirect('review_detail', review_id=review.id)


# РЕДАКТИРОВАНИЕ КОММЕНТАРИЕВ/ОТВЕТОВ
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    review = comment.review

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Комментарий обновлён.")
            return redirect('review_detail', review_id=review.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'moviesApp/edit_comment.html', {
        'form': form,
        'comment': comment
    })

# УВЕДОМЛЕНИЯ
def notifications_view(request):
    if not request.user.is_authenticated:
        html = render_to_string("moviesApp/notifications_login_required.html")
        return HttpResponse(html, status=200)

    notifications = Notification.objects.filter(
        recipient=request.user, removed=False
    ).order_by("-created_at")[:10]

    for n in notifications:
        if not n.is_read:
            n.is_read = True
            n.save()

    html = render_to_string("moviesApp/notifications_list.html", {"notifications": notifications})
    return HttpResponse(html)
