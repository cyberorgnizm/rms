from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(verbose_name="About Me", blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} ({self.matric_no})"

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    role = models.CharField(max_length=255, choices=(('Chef', 'Chef'), ('Delivery', 'Delivery')))

    def __str__(self):
        return f"{self.user} ({self.role})"
