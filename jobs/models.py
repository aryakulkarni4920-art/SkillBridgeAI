from django.db import models


class Job(models.Model):

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    salary = models.CharField(max_length=100)

    career = models.CharField(max_length=100)

    apply_link = models.URLField()

    def __str__(self):
        return self.title