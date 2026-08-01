from django.db import models


class Course(models.Model):

    career = models.CharField(max_length=100)

    title = models.CharField(max_length=200)

    platform = models.CharField(max_length=100)

    level = models.CharField(max_length=50)

    link = models.URLField()

    def __str__(self):
        return self.title