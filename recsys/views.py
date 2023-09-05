from django.shortcuts import render
from .models import News, Main_news


def news_list(request):
    return render(request, 'news_list.html', {'news':  News.objects.all(),
                                              'main': Main_news.objects.all()})


def news_one(request, id):
    print(id)
    article = News.objects.get(id=id)
    return render(request, 'news_one.html', {'article':  article})
