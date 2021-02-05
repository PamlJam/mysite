from django.db import models
from django.contrib.auth.models import User
# Django内置User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
class BlogType(models.Model):
# 博文分类
    type_name = models.CharField(max_length=20)
    def __str__(self):
    # 修改显示
        return self.type_name

class Blog(models.Model):
# 博文
    title = models.CharField(max_length=30)
    content =RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    # 外键关联到User 设置删除行为
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    # 外键关联到上面的博文分类,注意class的先后顺序，否则报错
    read_num = models.IntegerField(default=0)
    
    def __str__(self):
    # 修改显示
        return "<博客:%s>"%self.title
    
    class Meta:
        ordering=['-create_time']
        # 按照发表时间倒序排列
        