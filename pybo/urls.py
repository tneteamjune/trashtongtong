from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('', views.index, name='index'),
    path('notice/', views.notice, name='notice'),
    path('tip/', views.tip, name='tip'),
    path('mypage/', views.mypage, name='mypage'),
    path('greenpoint/', views.greenpoint, name='greenpoint'),
    path('points_list/', views.points_list, name='points_list'),
    path('greenpoint/<int:id>', views.points_detail, name="points_detail"),
    path('points_get/', views.points_get, name='points_get'),
    path('tip/plastic/' ,views.plastic, name='plastic'),
    path('tip/glass/' ,views.glass, name='glass'),
    path('tip/balpo/' ,views.balpo, name='balpo'),
    path('tip/vinyl/' ,views.vinyl, name='vinyl'),
    path('camera/' ,views.camera, name='camera'),
   ]