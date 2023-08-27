from django.shortcuts import render
from .models import News


def news_list(request):
    return render(request, 'news_list.html', {'news' :  News.objects.all()})
# def index(request):
#     return render(request, 'index.html')