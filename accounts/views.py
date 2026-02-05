from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Resume, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from jobs.models import  Application, SavedJob

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')

        if form.is_valid() and role:
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']  # ✅ ensure email saved
            user.save()

            # Profile created by signal
            profile = user.profile
            profile.role = role
            profile.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def resume_builder(request):
    resume, _ = Resume.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    )

    if request.method == 'POST':
        resume.full_name = request.POST.get('full_name')
        resume.email = request.POST.get('email')
        resume.phone = request.POST.get('phone')
        resume.address = request.POST.get('address')
        resume.website = request.POST.get('website')
        resume.summary = request.POST.get('summary')
        resume.skills = request.POST.get('skills')
        resume.experience = request.POST.get('experience')
        resume.education = request.POST.get('education')
        resume.projects = request.POST.get('projects')
        resume.certifications = request.POST.get('certifications')
        resume.languages = request.POST.get('languages')
        resume.extracurricular = request.POST.get('extracurricular')
        resume.references = request.POST.get('references')

        if request.FILES.get('photo'):
            resume.photo = request.FILES['photo']

        resume.save()
        return redirect('resume_preview')

    return render(request, 'resume/builder.html', {'resume': resume})


@login_required
def resume_preview(request):
    resume = Resume.objects.get(user=request.user)

    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []

    return render(request, 'resume/preview.html', {
        'resume': resume,
        'skills_list': skills_list,
    })

@login_required
def resume_download(request):
    resume = Resume.objects.get(user=request.user)

    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []

    template = get_template('resume/pdf.html')
    html = template.render({
        'resume': resume,
        'skills_list': skills_list,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response

@login_required
def candidate_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role != 'candidate':
        return redirect('/')

    context = {
        'applied_jobs': Application.objects.filter(applicant=request.user).count(),
        'saved_jobs': SavedJob.objects.filter(user=request.user).count(),
        'interviews': Application.objects.filter(
            applicant=request.user,
            status='shortlisted'
        ).count(),
    }
    return render(request, 'dashboard/candidate_dashboard.html', context)

@login_required
def candidate_overview(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role != 'candidate':
        return redirect('/')

    context = {
        'dashboard_page': 'dashboard/candidate/overview.html',
        'applied_count': Application.objects.filter(applicant=request.user).count(),
        'saved_count': SavedJob.objects.filter(user=request.user).count(),
        'shortlisted_count': Application.objects.filter(
            applicant=request.user,
            status='shortlisted'
        ).count(),
    }
    return render(request, 'dashboard/candidate_dashboard.html', context)


@login_required
def candidate_resume(request):
    resume = Resume.objects.filter(user=request.user).first()

    return render(request, 'dashboard/candidate_dashboard.html', {
        'dashboard_page': 'dashboard/candidate/resume.html',
        'resume': resume,
    })


@login_required
def candidate_applied_jobs(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__company')

    return render(request, 'dashboard/candidate_dashboard.html', {
        'dashboard_page': 'dashboard/candidate/applied_jobs.html',
        'applications': applications,
    })


@login_required
def candidate_saved_jobs(request):
    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job', 'job__company')

    return render(request, 'dashboard/candidate_dashboard.html', {
        'dashboard_page': 'dashboard/candidate/saved_jobs.html',
        'saved_jobs': saved_jobs,
    })


@login_required
def candidate_settings(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, 'dashboard/candidate_dashboard.html', {
        'dashboard_page': 'dashboard/candidate/settings.html',
        'profile': profile,
    })