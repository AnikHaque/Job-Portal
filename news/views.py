from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import News

@login_required
def create_news(request):
    profile = Profile.objects.get(user=request.user)

    if not (request.user.is_superuser or profile.role == 'employer'):
        return redirect('/')

    if request.method == 'POST':
        News.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            image=request.FILES.get('image'),
            author=request.user
        )
        return redirect('/')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/create_news.html',
        
    })