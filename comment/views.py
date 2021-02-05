from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from comment import models
# Create your views here.
def update_comment(request):
# 提交评论
    user = request.user
    text = request.POST.get('comment_text','')
    if text.strip() == '':
    # 如果评论区输入多个空格
        return HttpResponse('无内容')
    object_id = int(request.POST.get('object_id',''))
    # get返回值为字符串类型,记得转化为整形
    content_type = request.POST.get('content_type','')
    # "blog" <class 'str'>
    # content_type只能是app名：blog，comment
    model_app = ContentType.objects.get(model=content_type)
    # 根据app名，从数据表ContentType中的app列表中取出某一个app，比如blog
    model_class = model_app.model_class()
    # 从blog——app中取出一个特定的模型/类（判断对哪一类东西评论，比如博客Blog）
    model_obj = model_class.objects.get(pk=object_id)
    # 根据主键pk获取特定的对象(具体是对哪一篇博客评论)
    comment = Comment()
    #实例化一个Comment对象
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    # 将得到的信息填入刚刚新建的评论中
    comment.save()
    # 保存信息
    referer = request.META.get("HTTP_REFERER",'/')
    return redirect(referer)