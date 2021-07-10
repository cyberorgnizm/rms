from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Model for managing users registered on the platform"""

    avatar = models.ImageField(upload_to="users", verbose_name="upload photo", null=True, blank=True)
    bio = models.TextField(verbose_name="About", blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    """Model for managing college students records"""

    COLLEGE_LEVELS = (
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
    )

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    # TODO: move to separate model for dynamic creation
    DEPARTMENTS = (
        ('computer science', 'Computer Science'),
        ('mass communication', 'Mass communication'),
        ('anatomy', 'Anatomy')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_level = models.CharField(max_length=255, choices=COLLEGE_LEVELS, verbose_name="level")
    student_gender = models.CharField(max_length=1, choices=GENDER, verbose_name="gender")
    student_matric = models.CharField(max_length=255, verbose_name="matriculation number")
    student_department = models.CharField(max_length=255, choices=DEPARTMENTS, null=True)
    admission_year = models.DateField(null=True)
    student_address = models.TextField()

    def __str__(self):
        return f"{self.user}"


class Worker(models.Model):
    """Model for managing college cafeterias worker records"""

    WORKER_ROLES = (
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('delivery', 'Delivery'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    worker_role = models.CharField(max_length=255, choices=WORKER_ROLES, blank=True)

    def __str__(self):
        return f"{self.user} ({self.worker_role})"
