from django.urls import path
from . import views

urlpatterns = [
    # Add
    path('dashboard/add/', views.add_success_story, name='add_success_story'),

    # List (My stories)
    path('dashboard/', views.my_success_stories, name='my_success_stories'),

    # Edit
    path('dashboard/edit/<int:id>/', views.edit_success_story, name='edit_success_story'),

    # Delete
    path('dashboard/delete/<int:id>/', views.delete_success_story, name='delete_success_story'),
]
