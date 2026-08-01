from django.db import models
from django.contrib.auth.models import User


class Career(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    career_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class CareerCatalog(models.Model):

    career_name = models.CharField(max_length=100, unique=True)

    icon = models.CharField(max_length=10, default="💼")

    description = models.TextField(blank=True, default="")

    popular = models.BooleanField(default=True)

    def __str__(self):
        return self.career_name