from django.contrib import admin
from .models import Category, Article

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')

    fields = ['name']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_time', 'create_time', 'article_category')

    fields = ['title','article_category', 'content']

    list_filter = ['update_time']

    search_fields = ['title']

admin.site.register(Category ,CategoryAdmin)

admin.site.register(Article, ArticleAdmin)