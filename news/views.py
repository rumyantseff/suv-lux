from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user) 
            messages.success(request, 'You are successfully registered')
            return redirect('home') 
        else:
            messages.error(request, 'Error of registration')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'vladtest.ru@yandex.ru', ['vladik.rumyantsev@gmail.com'], fail_silently=False)
            if mail:                
                messages.success(request, 'Mail sent!')
                return redirect('contact') 
            else:
                messages.error(request, 'Error of sending')
        else:
            messages.error(request, 'Error of validation')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})

class HomeNews(MyMixin ,ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'Hello World'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Main page')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')



# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news':news, 
#         'title':'LuxCarsNews',
#     }
#     return render(request, template_name='news/index.html', context=context)
 



class News_By_Category(MyMixin ,ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'] ,is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin ,CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    # login_url = '/admin/'
    raise_exception = True


# def view_news(request, news_id):
#     # news_item = News.objects.get(id=news_id)    
#     news_item = get_object_or_404(News, id=news_id)
#     return render(request, 'news/view_news.html', {'news_item':news_item})   

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     # categories = Category.objects.all()
#     category = Category.objects.get(id=category_id)
#     return render(request, 'news/category.html', {'news':news, 
#                                                 # 'categories':categories,
#                                                 'category':category})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             # return redirect('home')
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form':form})