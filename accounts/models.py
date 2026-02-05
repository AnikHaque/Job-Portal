from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='resumes/photos/', blank=True, null=True)

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma separated skills")

    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    extracurricular = models.TextField(blank=True)
    references = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    


    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=150, blank=True)

    message = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name