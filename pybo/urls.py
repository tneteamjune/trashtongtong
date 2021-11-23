from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('notice/', views.notice, name='notice'),
    path('tip/', views.tip, name='tip'),
    path('mypage/', views.mypage, name='mypage'), 
   ]