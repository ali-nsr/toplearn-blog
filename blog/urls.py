from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home_page'),
    path('article/<slug>/', views.article_detail, name='article_detail'),
    path('article/add-comment/<article_pk>/', views.add_comment, name='add_comment'),
    path('article/add-comment/<article_pk>/<comment_pk>/', views.add_comment_reply, name='add_comment_reply'),
]
