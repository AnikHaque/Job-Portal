from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('resume/builder/', views.resume_builder, name='resume_builder'),
    path('resume/preview/', views.resume_preview, name='resume_preview'),
    path('resume/download/', views.resume_download, name='resume_download'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('dashboard/', views.candidate_overview, name='candidate_overview'),
    path('dashboard/resume/', views.candidate_resume, name='candidate_resume'),
    path('dashboard/applied/', views.candidate_applied_jobs, name='candidate_applied_jobs'),
    path('dashboard/saved/', views.candidate_saved_jobs, name='candidate_saved_jobs'),
    path('dashboard/settings/', views.candidate_settings, name='candidate_settings'),


]
