from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)

    object_id = models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    # 就是靠object_id，content_object这俩字段来筛选评论的！