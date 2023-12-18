from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import *
from newsapi import NewsApiClient
from datetime import date, timedelta

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, AddComment
from .models import News, Category
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title':"Следить за новостями",'url_name': 'follow_the_news'},
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
    prof = Profiles.objects.get(user=request.user.id)
    posts = News.objects.filter(profiles=prof.id)

    data = {
        'title': f'Мои новости',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'news/index.html', context=data)

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

def addcomment(request, post_slug):
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            new = News.objects.get(slug=post_slug)
            prof = Profiles.objects.get(user=request.user.id)
            posts = form.save(commit=False)
            # posts.news = new.id
            posts.user = prof
            posts.news = new
            posts.save()
            # id = request.POST.get("id")

            # form.fields['user'].choices = prof.id
            # form.fields['news'].choices = new.id

            # com = Comment.objects.get(id=id)
            # com = Comment.objects.get(news__slug=post_slug)
            # com.update(news=new.id)
            # com.update(user=prof.id)
            return redirect(reverse('post', kwargs={'post_slug': post_slug}))
    else:
        form = AddComment()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
        'form': form,
        'post_slug': post_slug,
    }
    return render(request, 'news/addcomment.html', context=data)


def post(request, post_slug):
    posts = News.objects.get(slug=post_slug)
    comment = Comment.objects.filter(news__id=posts.id)

    data = {
        'title': f'Пост {post_slug}',
        'menu': menu,
        'posts': posts,
        'comment': comment,
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

def proflogin(request):
    try:
        prof = Profiles(user=request.user)
        prof.save()
        return redirect('home')
    except Exception:
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('proflogin')

def logout_user(request):
    logout(request)
    return redirect('home')

def follow_the_news(request):
    current_date = date.today()
    yesterday = date.today() - timedelta(days=10)
    q1 = ['kylt', 'nauka', 'ekonom', 'sport']
    q2 = ['culture', 'everything', 'economy', 'sport']
    newsapi = NewsApiClient(api_key='ecdc4ef094694a738d238068eb2fcc4b')

    for x, y in zip(q1, q2):
        categor = Category.objects.get(slug=x)
        print(categor)
        maxResult = 100
        page = 0
        totalResult = 0
        while (maxResult * page <= totalResult):
            try:
                print(x)
                print(y)
                page += 1
                all_articles = newsapi.get_everything(q=str(y),
                                                      from_param='2023-12-14',
                                                      to='2023-12-18',
                                                      language='en',
                                                      page=page)
                if all_articles["status"] != "ok":
                    break

                articles = all_articles['articles']
                totalResult = all_articles["totalResults"]

                for i in articles:
                    print(i['title'])
                    title = i['title']
                    content = i['content']
                    #profile = Profiles.objects.get(user=1)
                    new = News(title=title, content=content, cat=categor)
                    slug = str(new.id) + '-news'
                    # new['slug'] = slug
                    new.save()
                    print(new)

            except Exception:
                break

    return redirect('home')






