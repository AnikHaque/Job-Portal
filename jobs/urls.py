from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('category/<slug:slug>/', views.jobs_by_category, name='jobs_by_category'),
    path('city/<str:city>/', views.jobs_by_city, name='jobs_by_city'),
    path('job/<int:id>/', views.job_detail, name='job_detail'),
    path('job/create/', views.create_job, name='create_job'),  # ✅ MUST
    path('job/<int:id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:id>/save/', views.toggle_save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('job/<int:id>/feature/', views.feature_job, name='feature_job'),
    path('job/<int:id>/feature/success/', views.feature_success, name='feature_success'),
    path('payments/', views.payment_history, name='payment_history'),
    path('payments/<int:id>/', views.payment_invoice, name='payment_invoice'),
    path('payments/<int:id>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('job/<int:id>/applicants/', views.applicant_list, name='applicant_list'),
    path(
    'application/<int:id>/<str:status>/',
    views.update_application_status,
    name='update_application_status'
),
  

]
