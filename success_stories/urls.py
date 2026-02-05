from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/add', views.add_success_story, name='add_success_story'),
]
