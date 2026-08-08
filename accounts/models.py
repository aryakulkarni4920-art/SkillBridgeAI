from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = CloudinaryField(
        "profile_picture",
        default="profile_pictures/default"
    )

    def __str__(self):
        return self.user.username