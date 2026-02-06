from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import News
from accounts.models import Profile


@login_required
def create_news(request):
    profile = Profile.objects.get(user=request.user)

    # Only admin or employer can post news
    if not (request.user.is_superuser or profile.role == 'employer'):
        return redirect('/')

    if request.method == 'POST':
        news = News(
            title=request.POST.get('title'),
            summary=request.POST.get('summary'),
            content=request.POST.get('content'),
            status=request.POST.get('status', 'draft'),
            meta_title=request.POST.get('meta_title', ''),
            meta_description=request.POST.get('meta_description', ''),
            featured_image=request.FILES.get('featured_image'),
            author=request.user
        )
        news.save()

        return redirect('news_detail', slug=news.slug)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/create_news.html',
    })


def news_detail(request, slug):
    news = get_object_or_404(
        News,
        slug=slug,
        status='published'
    )
    return render(request, 'news/news_detail.html', {
        'news': news
    })
