from django.core import paginator
from django.http import response
from .models import Blog
from .models import BlogType
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render


from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


def common_data(bloglists):
# 可用于返回公共信息  
    context={}
    return context

def gethot():
    blogs=Blog.objects.all().order_by('-read_num')
    # 根据阅读数量降序排列，获取所有博文
    readmost_blog=blogs.first()
    # 阅读次数最多的博客（排序后的第一篇）
    return readmost_blog

def blogList(request):
    context={}
    hot=cache.get('hot')
    # 获取缓存数据(热门文章),类似于字典取值，get默认值为none
    if hot is None:
        hot=gethot()
        # 重新获取
        cache.set('hot',hot,3600)
        # 重新设置缓存,类似于字典存值
        # parm3 缓存有效时间为1h=3600s
        print('recalculate')
        # 若在服务器没有显示，则代表使用了缓存
    context['hot']=hot
    allblogs=Blog.objects.all()
    # blog/?page=1
    paginator=Paginator(allblogs,8)
    # 获取一个分页器>>以10为单位分页
    page_num=request.GET.get("page",1) # GET请求的参数
    # 传过来的页面参数（无输入默认为1）
    p=paginator.get_page(page_num) # 得到具体的一页,已处理意外输入
    context['blogs']=p
    # 传入具体的某一个page

    types=BlogType.objects.all()
    # 获取所有的博客分类
    for t in types:
        t_cnt= Blog.objects.filter(blog_type=t).count()
        # 分类计数
        t.cnt=t_cnt
        # 给每一个t对象都手动加一个属性,形成关联
    context['types']=types

    context['blogdates']= Blog.objects.dates('create_time','month',order='DESC')
    # parm1 字段 parm2 按月分类 parm3 倒序
    # 返回一个查询 QuerySet 返回所有符合的日期
    return render_to_response('blog/blogList.html',context)

def blogDetail(request,blog_pk):
    context={}
    blog=get_object_or_404(Blog,id=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    # 通过model或者model的实例来寻找ContentType类型
    comments = Comment.objects.filter(content_type=blog_content_type,object_id = blog.pk)
    # 靠object_id，content_object这俩字段来筛选评论的！
    context["comments"] = comments
    if not request.COOKIES.get('blog%s_read'%blog_pk):
        blog.read_num+=1
        blog.save()
    context['blog']=blog
    context['pre_blog']=Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['nxt_blog']=Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render(request,'blog/blogDetail.html',context)
    response.set_cookie('blog%s_read'%blog_pk,'true',max_age=60)
    return response

    
def blogType(request,blogtype_pk):
# 分类展示
    context={}
    btype=get_object_or_404(BlogType,pk=blogtype_pk)
    # 先确定博客类型
    context['blogs']=Blog.objects.filter(blog_type=btype)
    # 筛选得到类型符合的所有博客
    context['blogs_type'] = btype 
    return render_to_response('blog/blogType.html',context)


def blogDate(request,year,month):
    context={}
    blogs=Blog.objects.filter(create_time__year=year,create_time__month=month)
    context['blogs']=blogs
    context['year']=year
    context['month']=month
    return render_to_response('blog/blogDate.html',context)