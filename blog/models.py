from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length = 30)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add = True)
    update_time = models.DateTimeField(auto_now = True)
    article_category = models.ForeignKey(Category, on_delete = models.DO_NOTHING)
    def __str__(self):
        return self.title