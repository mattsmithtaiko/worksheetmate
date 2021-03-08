from django.urls import path

from . import views

app_name= 'questions'
urlpatterns = [
    path('index', views.index, name='index'),
    path('add', views.add, name='add'),
    path('add/single', views.add_singlequestion, name='add_singlequestion'),
    path('add/multipart', views.add_multipartquestion, name='add_multipartquestion'),
    path('search_category', views.search_category, name='search_category'),
]
