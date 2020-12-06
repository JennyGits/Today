from django.urls import path
from . import  views

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('last_result_page/', views.last_result_page, name='last_result_page')
]


app_name = 'polls'