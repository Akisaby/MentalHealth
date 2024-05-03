
from django.shortcuts import render, get_object_or_404
from .models import Article
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article/article_list.html',{'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    articles = Article.objects.all()
    context ={'articles': articles,'article': article}
    return render(request, 'article/article_detail.html',context)


def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def pricing_view(request):
    return render(request, 'pricing.html')

