from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(verbose_name="About Me", blank=True, null=True)
    matric = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
