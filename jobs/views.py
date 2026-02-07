from django.contrib import messages
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from companies.models import Company
from django.db.models import Count
from jobs.models import Job,Category
from .models import Job, Application, SavedJob
from success_stories.models import SuccessStory
from news.models import News
from django.db.models import Q
from django.utils import timezone
from .utils import FEATURED_PACKAGES, apply_featured
from .models import Payment
from .utils import generate_invoice_pdf
from .utils import send_application_email
from django.db.models.functions import Lower

stripe.api_key = settings.STRIPE_SECRET_KEY

# def home(request):
#     jobs = Job.objects.all().order_by('-created_at')

#     categories = Category.objects.annotate(
#         total_jobs=Count('jobs')
#     )

#     return render(request, 'jobs/home.html', {
#         'jobs': jobs,
#         'categories': categories,
#     })
    
# def jobs_by_category(request, slug):
#     category = Category.objects.get(slug=slug)
#     jobs = Job.objects.filter(category=category)

#     return render(request, 'jobs/jobs_by_category.html', {
#         'category': category,
#         'jobs': jobs,
#     })

# def job_list(request):
#     # ⏳ Auto-unfeature expired jobs
#     Job.objects.filter(
#         is_featured=True,
#         featured_until__lt=timezone.now()
#     ).update(is_featured=False, featured_until=None)

#     # 🔹 Base queryset
#     jobs = Job.objects.all().order_by('-created_at')

#     # 🔹 Filters from URL
#     keyword = request.GET.get('q')
#     location = request.GET.get('location')
#     job_type = request.GET.get('job_type')
#     category_slug = request.GET.get('category')

#     # 🔍 Keyword search (title + company)
#     if keyword:
#         jobs = jobs.filter(
#             Q(title__icontains=keyword) |
#             Q(company__name__icontains=keyword)
#         )

#     # 📍 Location filter
#     if location:
#         jobs = jobs.filter(location__icontains=location)

#     # 🕒 Job type filter
#     if job_type:
#         jobs = jobs.filter(job_type=job_type)

#     # 🗂️ Category filter
#     if category_slug:
#         jobs = jobs.filter(category__slug=category_slug)

#     # ⭐ Featured & Normal split (AFTER all filters)
#     featured_jobs = jobs.filter(is_featured=True)
#     normal_jobs = jobs.filter(is_featured=False)

#     # 📦 Categories (always show on page)
#     categories = Category.objects.annotate(
#         total_jobs=Count('jobs')
#     )

#     return render(request, 'jobs/job_list.html', {
#         'featured_jobs': featured_jobs,
#         'jobs': normal_jobs,

#         # filters (for keeping input values)
#         'keyword': keyword,
#         'location': location,
#         'job_type': job_type,
#         'active_category': category_slug,

#         # categories
#         'categories': categories,
#     })


def job_list(request):
    # ⏳ Expired featured job auto-disable
    Job.objects.filter(
        is_featured=True,
        featured_until__lt=timezone.now()
    ).update(is_featured=False, featured_until=None)

    # 🔹 Base queryset
    jobs_qs = Job.objects.all().order_by('-created_at')

    # 🔍 Filters
    keyword = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')

    if keyword:
        jobs_qs = jobs_qs.filter(
            Q(title__icontains=keyword) |
            Q(company__name__icontains=keyword)
        )

    if location:
        jobs_qs = jobs_qs.filter(location__icontains=location)

    if job_type:
        jobs_qs = jobs_qs.filter(job_type=job_type)

    # ⭐ Featured & normal split
    featured_jobs = jobs_qs.filter(is_featured=True)
    normal_jobs = jobs_qs.filter(is_featured=False)

    # 🗂️ Categories for cards
    categories = Category.objects.annotate(
        total_jobs=Count('jobs')
    )
    companies = Company.objects.annotate(
    total_jobs=Count('job')
)
    
    # 🌆 Cities with job count
    cities = (
    Job.objects
    .exclude(location__isnull=True)
    .exclude(location__exact="")
    .values(city=Lower('location'))
    .annotate(total_jobs=Count('id'))
    .order_by('-total_jobs')
)
    news_list = News.objects.all().order_by('-created_at')[:5]
    success_stories = None
    if request.user.is_authenticated:
        role = request.user.profile.role
        success_stories = SuccessStory.objects.filter(
            story_type=role
        ).order_by("-created_at")[:6]
    context = {
        'featured_jobs': featured_jobs,
        'jobs': normal_jobs,
        'categories': categories,
        'companies': companies,
        'cities': cities,
        'news_list': news_list,
        "success_stories": success_stories,
        # keep filters in UI
        'keyword': keyword,
        'location': location,
        'job_type': job_type,

    }

    return render(request, 'jobs/job_list.html', context)

def all_jobs(request):
    jobs = Job.objects.all()

    q = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    company = request.GET.get('company')

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(company__name__icontains=q)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if company:
        jobs = jobs.filter(company_id=company)

    context = {
        'jobs': jobs,
        'job_types': Job.JOB_TYPE,
        'companies': Company.objects.all(),
        'selected_job_type': job_type,
        'selected_company': company,
        'keyword': q,
        'location': location,
    }

    return render(request, 'jobs/alljobs.html', context)



def jobs_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    jobs = Job.objects.filter(
        category=category
    ).order_by('-created_at')

    return render(request, 'jobs/jobs_by_category.html', {
        'category': category,
        'jobs': jobs,
    })
def jobs_by_city(request, city):
    jobs = Job.objects.filter(
        location__iexact=city
    ).order_by('-created_at')

    return render(request, 'jobs/jobs_by_city.html', {
        'city': city,
        'jobs': jobs,
    })

# ✅ Job Detail Page
def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'jobs/job_detail.html', {'job': job})


# ✅ Employer Only – Create Job
@login_required
def create_job(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Only employer can post job
    if profile.role != 'employer':
        return redirect('/')

    # Employer must have company
    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        return redirect('create_company')

    if request.method == 'POST':
        Job.objects.create(
            company=company,
            title=request.POST['title'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary=request.POST.get('salary', ''),
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            deadline=request.POST['deadline']
        )
        return redirect('company_detail')

    return render(request, 'jobs/create_job.html')
from .models import Application

@login_required
def apply_job(request, id):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Only candidate can apply
    if profile.role != 'candidate':
        return redirect('job_detail', id=id)

    job = get_object_or_404(Job, id=id)

    # Prevent duplicate apply
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return render(request, 'jobs/already_applied.html', {'job': job})

    if request.method == 'POST':
        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=request.FILES['resume'],
            cover_letter=request.POST.get('cover_letter', '')
        )
        return render(request, 'jobs/apply_success.html', {'job': job})

    return render(request, 'jobs/apply_job.html', {'job': job})
@login_required
def create_job(request):
    company = Company.objects.get(owner=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        Job.objects.create(
            company=company,
            title=request.POST['title'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary=request.POST.get('salary'),
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            deadline=request.POST['deadline'],
            category_id=request.POST.get('category')
        )
        return redirect('company_detail')

    return render(request, 'jobs/create_job.html', {
        'categories': categories
    })

@login_required
def applicant_list(request, id):
    job = get_object_or_404(
        Job,
        id=id,
        company__owner=request.user
    )

    applications = Application.objects.filter(job=job)

    return render(request, 'jobs/applicant_list.html', {
        'job': job,
        'applications': applications,
    })
@login_required
def update_application_status(request, id, status):
    application = get_object_or_404(
        Application,
        id=id,
        job__company__owner=request.user
    )

    if status in ['shortlisted', 'rejected']:
        application.status = status
        application.save()

    return redirect('applicant_list', id=application.job.id)


@login_required
def saved_jobs(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.role != 'candidate':
        return redirect('/')

    saved = SavedJob.objects.filter(user=request.user) # type: ignore
    return render(request, 'jobs/saved_jobs.html', {'saved': saved})
from .models import SavedJob

@login_required
def toggle_save_job(request, id):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Only candidate can save job
    if profile.role != 'candidate':
        return redirect('job_detail', id=id)

    job = get_object_or_404(Job, id=id)

    saved = SavedJob.objects.filter(user=request.user, job=job)

    if saved.exists():
        saved.delete()   # Unsave
    else:
        SavedJob.objects.create(user=request.user, job=job)

    return redirect('job_detail', id=id)

@login_required
def feature_job(request, id):
    job = get_object_or_404(Job, id=id, company__owner=request.user)

    if request.method == 'POST':
        package = request.POST.get('package')

        if package in FEATURED_PACKAGES:
            pack = FEATURED_PACKAGES[package]

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'bdt',
                        'product_data': {
                            'name': f'Featured Job ({pack["days"]} days)',
                        },
                        'unit_amount': pack['price'] * 100,
                    },
                    'quantity': 1,
                }],
                success_url=request.build_absolute_uri(
    f'/job/{job.id}/feature/success/?days={pack["days"]}&session_id={{CHECKOUT_SESSION_ID}}'
),

                cancel_url=request.build_absolute_uri('/company/'),
            )

            return redirect(session.url)

    return render(request, 'jobs/feature_job.html', {
        'job': job,
        'packages': FEATURED_PACKAGES,
    })

@login_required
def feature_success(request, id):
    job = get_object_or_404(Job, id=id, company__owner=request.user)

    days = int(request.GET.get('days', 0))
    session_id = request.GET.get('session_id', '')

    if days:
        apply_featured(job, days)

        Payment.objects.create(
            user=request.user,
            job=job,
            amount=FEATURED_PACKAGES[str(days)]['price'],
            days=days,
            stripe_session_id=session_id,
            status='paid'
        )

        messages.success(
            request,
            f'Payment successful! Job featured for {days} days.'
        )

    return redirect('company_detail')

@login_required
def payment_history(request):
    payments = Payment.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'jobs/payment_history.html', {
        'payments': payments
    })

@login_required
def payment_invoice(request, id):
    payment = get_object_or_404(
        Payment,
        id=id,
        user=request.user
    )

    return render(request, 'jobs/invoice.html', {
        'payment': payment
    })

@login_required
def invoice_pdf(request, id):
    payment = get_object_or_404(
        Payment,
        id=id,
        user=request.user
    )
    return generate_invoice_pdf(payment)

@login_required
def update_application_status(request, id, status):
    application = get_object_or_404(
        Application,
        id=id,
        job__company__owner=request.user
    )

    if status in ['shortlisted', 'rejected']:
        application.status = status
        application.save()
        print("DEBUG: update_application_status called")
        print("Candidate email:", application.applicant.email)
        # 📧 Send email to candidate
        send_application_email(application, status)


    return redirect('applicant_list', id=application.job.id)