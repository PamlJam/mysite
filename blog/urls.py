from django.urls import path
from . import views
#博客内容 http://localhost:8000/blog/1
#博客列表 http://localhost:8000/

urlpatterns =[
    path('',views.blogList),
    path('<int:blog_pk>',views.blogDetail,name='x'),
    # int:blog_pk由用户输入，传参给blogDetail的blog_pk
    # 二者必须命名必须保持一致
    path('type/<int:blogtype_pk>',views.blogType),
    path('date/<int:year>/<int:month>',views.blogDate),
]