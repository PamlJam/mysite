from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('search/', views.search, name='searchArticle'),
    
    path('article/', views.ArticleListView.as_view(), name='ArticleList'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='ArticleDetail'),
    
    path('article/<int:pk>/download/', views.download, name='DownloadArticle'),

    path('category/', views.CategoryListView.as_view(), name='CategoryList'),    
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='CategoryDetail'),

]
