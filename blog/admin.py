from django.contrib import admin
from .models import *


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'status', 'created_date', 'updated_date', 'admin_thumbnail']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'reply']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Slider)
admin.site.register(Comment, CommentAdmin)
