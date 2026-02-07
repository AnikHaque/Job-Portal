from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    # ===== List view =====
    list_display = (
        'title',
        'author',
        'status',
        'created_at',
        'published_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('title', 'summary', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    # slug auto from title
    prepopulated_fields = {'slug': ('title',)}

    # ===== Admin-only permissions =====
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
