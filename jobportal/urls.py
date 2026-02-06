from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('companies.urls')),
    path('', include('jobs.urls')),   # ✅ MUST
    path('company/', include('companies.urls')),
    path('', include('news.urls')),
    path('success-stories/', include('success_stories.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
