from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Article, Category, Slider, Comment
from .forms import CommentForm, CommentReplyForm
from django.contrib import messages


# Create your views here.
def home(request):
    articles = Article.objects.filter(status='p')[:3]
    latest_articles = Article.objects.filter(status='p').order_by('-created_date')[:3]
    categories = Category.objects.all()[:6]
    sliders = Slider.objects.all()
    context = {
        'articles': articles,
        'latest_articles': latest_articles,
        'categories': categories,
        'sliders': sliders,
    }
    return render(request, 'blog/home.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    latest_articles = Article.objects.filter(status='p').order_by('-created_date')[:3]
    categories = Category.objects.all()[:6]
    comment_form = CommentForm()
    comment_reply_form = CommentReplyForm()
    comments = Comment.objects.filter(article_id=article.id, is_reply=False).order_by('-created_date')
    comment_count = Comment.objects.filter(article_id=article.id).count()
    context = {
        'article': article,
        'latest_articles': latest_articles,
        'categories': categories,
        'comment_form': comment_form,
        'comments': comments,
        'comment_reply_form': comment_reply_form,
        'comment_count': comment_count
    }
    return render(request, 'blog/article_detail.html', context)


def add_comment(request, article_pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user_id=request.user.id, article_id=article_pk,
                                   content=form.cleaned_data.get('content'))
        messages.success(request, 'Your Comment Added Successfully')
        return redirect(request.META.get('HTTP_REFERER'))


def add_comment_reply(request, article_pk, comment_pk):
    if request.method == 'POST':
        reply_form = CommentReplyForm(request.POST)
        if reply_form.is_valid():
            Comment.objects.create(user_id=request.user.id, article_id=article_pk, reply_id=comment_pk,
                                   content=reply_form.cleaned_data.get('content'), is_reply=True)
            messages.warning(request, 'your Reply Added Successfully')
            return redirect(request.META.get('HTTP_REFERER'))
