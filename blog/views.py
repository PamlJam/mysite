from django.views import generic
from .models import Article, Category
from markdown import markdown
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.http import HttpResponse


allCategory = Category.objects.all()

class ArticleDetailView(generic.DetailView):
    model = Article

    def get_object(self, **kwargs):
        a = Article.objects.get(id = self.kwargs['pk'])
        a.content = markdown(a.content,extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return a

class ArticleListView(generic.ListView):
    model = Article
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allCategory'] = allCategory
        return context

class CategoryDetailView(generic.DetailView):
    model = Category

class CategoryListView(generic.ListView):
    model = Category


def search(request):
    q = request.GET.get('q')
    # 与表单 input 标签 name 属性对应
    
    Q1 = Q(title__icontains = q)
    Q2 = Q(content__icontains = q)
    # 根据文章标题与内容进行关键词模糊搜索

    result = Article.objects.filter(Q1 | Q2)

    context = {
        'article_list' : result,
    }

    return render(request,'blog/search_result.html',context)


def download(request,**kwargs):
    a = get_object_or_404(Article,id = kwargs['pk'])
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + "download.txt"
    response.write(a.content)
    return response