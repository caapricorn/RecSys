from django.shortcuts import render
from .models import News, Top_news


def news_list(request):
    return render(request, 'news_list.html', {'news':  News.objects.all(),
                                              'top': Top_news.objects.all()})
# def index(request):
#     return render(request, 'index.html')