from django.urls import path
from . import views

urlpatterns = [
     path('news/create/', views.create_news, name='create_news'),
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]
