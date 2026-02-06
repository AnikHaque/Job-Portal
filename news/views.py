from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import News
from accounts.models import Profile


@login_required
def create_news(request):
    profile = Profile.objects.get(user=request.user)

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
        return redirect('my_news')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/create_news.html',
    })


@login_required
def my_news(request):
    profile = Profile.objects.get(user=request.user)

    if not (request.user.is_superuser or profile.role == 'employer'):
        return redirect('/')

    news_list = News.objects.filter(author=request.user)

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/list.html',
        'news_list': news_list
    })


@login_required
def edit_news(request, id):
    news = get_object_or_404(News, id=id, author=request.user)

    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.summary = request.POST.get('summary')
        news.content = request.POST.get('content')
        news.status = request.POST.get('status', 'draft')
        news.meta_title = request.POST.get('meta_title', '')
        news.meta_description = request.POST.get('meta_description', '')

        if request.FILES.get('featured_image'):
            news.featured_image = request.FILES.get('featured_image')

        news.save()
        return redirect('my_news')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/edit_news.html',
        'news': news
    })


@login_required
def delete_news(request, id):
    news = get_object_or_404(News, id=id, author=request.user)

    if request.method == 'POST':
        news.delete()
        return redirect('my_news')

    return render(request, 'dashboard/employer_dashboard.html', {
        'dashboard_page': 'news/delete_news.html',
        'news': news
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
