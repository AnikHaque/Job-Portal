from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SuccessStory

@login_required
def add_success_story(request):
    profile = request.user.profile  # role: candidate / employer

    if request.method == "POST":
        SuccessStory.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            story=request.POST.get("story"),
            company_name=request.POST.get("company_name", ""),
            story_type=profile.role
        )
        return redirect("job_list")

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'success_stories/add.html',
        
    })