from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
    path('company/', views.company_detail, name='company_detail'),
    path('company/<int:id>/', views.company_public_detail, name='company_public_detail'),
    path('company/create/', views.create_company, name='create_company'),
    path('analytics/', views.employer_analytics, name='employer_analytics'),
    path('<int:company_id>/', views.company_jobs, name='company_jobs'),
    path('<int:company_id>/jobs/', views.jobs_by_company, name='jobs_by_company'),
    path('dashboard/', views.employer_overview, name='employer_overview'),
    path('dashboard/company/', views.company_profile, name='company_profile'),
    path('dashboard/jobs/', views.employer_jobs, name='employer_jobs'),
    path('dashboard/applicants/', views.employer_applicants, name='employer_applicants'),
    path('dashboard/payments/', views.employer_payments, name='employer_payments'),
    path('dashboard/analytics/', views.employer_analytics, name='employer_analytics'),
    path('dashboard/post-job/', views.employer_post_job, name='employer_post_job'),


]
