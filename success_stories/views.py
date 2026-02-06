from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SuccessStory


@login_required
def add_success_story(request):
    profile = request.user.profile

    if request.method == "POST":
        SuccessStory.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            story=request.POST.get("story"),
            company_name=request.POST.get("company_name", ""),
            story_type=profile.role
        )
        return redirect("my_success_stories")

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'success_stories/add.html',
    })


@login_required
def edit_success_story(request, id):
    story = get_object_or_404(SuccessStory, id=id, user=request.user)

    if request.method == "POST":
        story.title = request.POST.get("title")
        story.story = request.POST.get("story")
        story.company_name = request.POST.get("company_name", "")
        story.save()

        return redirect("my_success_stories")

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'success_stories/edit.html',
        'story': story
    })


@login_required
def delete_success_story(request, id):
    story = get_object_or_404(SuccessStory, id=id, user=request.user)

    if request.method == "POST":
        story.delete()
        return redirect("my_success_stories")

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'success_stories/delete.html',
        'story': story
    })


@login_required
def my_success_stories(request):
    stories = SuccessStory.objects.filter(user=request.user)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'success_stories/list.html',
        'stories': stories
    })
