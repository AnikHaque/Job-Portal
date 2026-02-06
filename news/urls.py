from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Dashboard routes FIRST
    path('dashboard/', views.my_news, name='my_news'),
    path('dashboard/edit/<int:id>/', views.edit_news, name='edit_news'),
    path('dashboard/delete/<int:id>/', views.delete_news, name='delete_news'),

    # 🔹 Create (old route – keep)
    path('news/create/', views.create_news, name='create_news'),

    # 🔹 Slug route ALWAYS LAST
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]
