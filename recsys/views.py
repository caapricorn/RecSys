from django.shortcuts import render
from .models import News, Main_news


def news_list(request):
    return render(request, 'news_list.html', {'news':  News.objects.all(),
                                              'main': Main_news.objects.all()})
# def index(request):
#     return render(request, 'index.html')