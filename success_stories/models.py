from django.db import models
from django.contrib.auth.models import User

class SuccessStory(models.Model):
    STORY_TYPE = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    story = models.TextField()
    company_name = models.CharField(max_length=150, blank=True)
    story_type = models.CharField(max_length=20, choices=STORY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
