from django.contrib import admin
from .models import Job,Application,Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'logo')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company',
        'category',      # ✅ এখানে যোগ
        'job_type',
        'deadline',
        'is_featured'
    )

    list_editable = ('is_featured',)
    list_filter = ('category', 'job_type', 'company')  # ✅ filter
    search_fields = ('title', 'company__name')
    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at')
