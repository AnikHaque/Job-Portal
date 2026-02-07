from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json

from accounts.models import Profile
from jobs.models import Job, Application, Payment, Category
from .models import Company
from django.db.models import Q, Count

# -----------------------------
# Create Company
# -----------------------------
@login_required
def create_company(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Only employer can create company
    if profile.role != 'employer':
        return redirect('/')

    # If company already exists, go to dashboard
    if Company.objects.filter(owner=request.user).exists():
        return redirect('company_detail')

    if request.method == 'POST':
        Company.objects.create(
            owner=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            website=request.POST.get('website', ''),
            location=request.POST['location'],
            logo=request.FILES.get('logo')
        )
        return redirect('company_detail')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'companies/create_company.html',
    })

def company_list(request):
    companies = Company.objects.annotate(
        total_jobs=Count('job')
    ).order_by('-id')

    # Filters
    keyword = request.GET.get('q')
    location = request.GET.get('location')

    if keyword:
        companies = companies.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    if location:
        companies = companies.filter(location__icontains=location)

    context = {
        'companies': companies,
        'keyword': keyword,
        'location': location,
    }

    return render(request, 'companies/company_list.html', context)

# -----------------------------
# Company Dashboard
# -----------------------------
@login_required
def company_detail(request):
    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        return redirect('create_company')

    jobs = Job.objects.filter(company=company).order_by('-created_at')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'companies/company_detail.html',
        'company': company,
        'jobs': jobs,
    })

def company_public_detail(request, id):
    company = get_object_or_404(Company, id=id)
    jobs = Job.objects.filter(company=company).order_by('-created_at')

    return render(request, 'companies/company_public_detail.html', {
        'company': company,
        'jobs': jobs,
    })


def company_jobs(request, company_id):
    company = Company.objects.get(id=company_id)
    jobs = Job.objects.filter(company=company)

    return render(request, 'companies/company_jobs.html', {
        'company': company,
        'jobs': jobs,
    })


def jobs_by_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    jobs = Job.objects.filter(
        company=company
    ).order_by('-created_at')

    return render(request, 'companies/jobs_by_company.html', {
        'company': company,
        'jobs': jobs,
    })

# -----------------------------
# Employer Analytics
# -----------------------------
@login_required
def employer_analytics(request):
    profile = Profile.objects.get(user=request.user)

    # Safety check
    if profile.role != 'employer':
        return redirect('/')

    company = Company.objects.get(owner=request.user)

    jobs = Job.objects.filter(company=company)

    total_jobs = jobs.count()

    total_applications = Application.objects.filter(
        job__company=company
    ).count()

    shortlisted = Application.objects.filter(
        job__company=company,
        status='shortlisted'
    ).count()

    rejected = Application.objects.filter(
        job__company=company,
        status='rejected'
    ).count()

    # Job-wise applicants
    job_stats = jobs.annotate(applicants=Count('applications'))

    # Chart.js data (JSON safe)
    job_titles = [job.title for job in job_stats]
    applicant_counts = [job.applicants for job in job_stats]

    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'job_stats': job_stats,

        # Chart.js
        'job_titles': json.dumps(job_titles),
        'applicant_counts': json.dumps(applicant_counts),
        'status_counts': json.dumps([shortlisted, rejected]),
    }

    return render(request, 'companies/employer_analytics.html', context)

# -----------------------------
# Employer Dashboard
# -----------------------------
@login_required
def employer_overview(request):
    company = Company.objects.get(owner=request.user)

    context = {
        'dashboard_page': 'dashboard/employer/overview.html',
        'total_jobs': Job.objects.filter(company=company).count(),
        'total_applications': Application.objects.filter(
            job__company=company
        ).count(),
        'shortlisted': Application.objects.filter(
            job__company=company, status='shortlisted'
        ).count(),
    }
    return render(request, 'dashboard/employer_dashboard.html', context)


@login_required
def company_profile(request):
    company = Company.objects.get(owner=request.user)
    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/company_profile.html',
        'company': company,
    })


@login_required
def employer_jobs(request):
    company = Company.objects.get(owner=request.user)
    jobs = Job.objects.filter(company=company)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/jobs.html',
        'jobs': jobs,
    })


@login_required
def employer_applicants(request):
    company = Company.objects.get(owner=request.user)
    applications = Application.objects.filter(job__company=company)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/applicants.html',
        'applications': applications,
    })


@login_required
def employer_payments(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/payments.html',
        'payments': payments,
    })


@login_required
def employer_analytics(request):
    company = Company.objects.get(owner=request.user)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/analytics.html',
        'total_jobs': Job.objects.filter(company=company).count(),
        'total_applications': Application.objects.filter(job__company=company).count(),
        'shortlisted': Application.objects.filter(job__company=company, status='shortlisted').count(),
        'rejected': Application.objects.filter(job__company=company, status='rejected').count(),
    })

@login_required
def employer_post_job(request):
    company = Company.objects.get(owner=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        Job.objects.create(
            company=company,
            category=Category.objects.get(id=request.POST['category']),
            title=request.POST['title'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary=request.POST.get('salary'),
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            deadline=request.POST['deadline'],
        )
        return redirect('employer_jobs')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'dashboard/employer/post_job.html',
        'categories': categories,
    })