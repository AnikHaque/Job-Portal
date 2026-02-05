from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
