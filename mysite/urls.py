from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('userprofile/', include('userprofile.urls', namespace = 'userprofile')),
]