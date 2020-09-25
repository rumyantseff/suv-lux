from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import News, Category


# Create your views here.
def index(request):
    news = News.objects.order_by('-created_at')
    # categories = Category.objects.all()
    context = {
        'news':news, 
        'title':'LuxCarsNews',
        # 'categories': categories,
    }
    return render(request, template_name='news/index.html', context=context)
 
def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    # categories = Category.objects.all()
    category = Category.objects.get(id=category_id)
    return render(request, 'news/category.html', {'news':news, 
                                                # 'categories':categories,
                                                'category':category})

def view_news(request, news_id):
    # news_item = News.objects.get(id=news_id)    
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news/view_news.html', {'news_item':news_item})                                            