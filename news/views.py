from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import *

from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import News, Category
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Мои статьи", 'url_name': 'my_articles'},]

def index(request):
    posts = News.objects.filter(is_published=True)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0
    }
    return render(request, 'news/index.html', context=data)

# def base(request):
#     data = {
#         "menu": menu,
#     }
#     return render(request, 'news/base.html', context= data)

def my_articles(request):
    return HttpResponse('Мои статьи')

def about(request):
   return HttpResponse('о сайте')

def add_page(request):
    return HttpResponse('Добавить статью')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Статьи')
def register(request):
    return HttpResponse('red')


def reviews(request, post_id):
    return HttpResponse(f"Отзывы на пост с id={post_id}")

def cat(request, cat_slug):
    cats = Category.objects.filter(slug=cat_slug)
    posts = News.objects.filter(cat__slug=cat_slug)

    data = {
        'title': f'Новости категории',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'news/index.html', context=data)
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            us_id = request.user.id
            sl = request.POST.get("slug")
            nws = News.objects.filter(slug=sl)
            nws.update(profiles_id=us_id)
            return redirect('home')

    else:
        form = AddPostForm()

    return render(request, 'news/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def addpage_save(request):
    us_id = request.user.id
    sl = request.POST.get("slug")
    nws = News.objects.get(slug=sl)
    nws.objects.update(profiles_id=us_id)
    nws.save()

    posts = News.objects.filter(is_published=True)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0
    }
    return render(request, 'news/index.html', context=data)


def post(request, post_slug):
    posts = News.objects.get(slug=post_slug)

    data = {
        'title': f'Пост {post_slug}',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'news/post.html', context=data)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')


