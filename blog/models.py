from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.shortcuts import reverse

User = get_user_model()


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='d')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def admin_thumbnail(self):
        return format_html('<img style="width:80px;" src="{}">'.format(self.image.url))

    admin_thumbnail.short_description = 'image'

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.slug])


class Slider(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.article.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    content = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rely_comments')
    is_reply = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
