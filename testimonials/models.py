from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
  

    def __str__(self):
        return f"{self.user.username} ({self.rating}★)"
