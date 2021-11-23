from django.contrib import admin
from django.urls import path, include
from pybo import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
    path('notice/', views.notice, name='notice'),
    path('tip/', views.tip, name='tip'),
    path('mypage/', views.mypage, name='mypage'),
    path('greenpoint/', views.greenpoint, name='greenpoint'),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
