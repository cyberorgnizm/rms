import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings



class User(AbstractUser):
    """Model for managing users registered on the platform"""

    avatar = models.ImageField(upload_to="users", verbose_name="upload photo", null=True, blank=True)
    bio = models.TextField(verbose_name="About", blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Department(models.Model):
    """Model for managing college departments"""

    FACULTIES = (
        ('Science & Technology', 'science & technology'),
        ('Humanities', 'humanities'),
        ('Medical Sciences', 'medical sciences')
    )
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255, choices=FACULTIES)

    def __str__(self):
        return self.name


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


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=255, choices=COLLEGE_LEVELS, verbose_name="level")
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name="gender")
    matric = models.CharField(max_length=255, verbose_name="matriculation number")
    department = models.ForeignKey('Department', related_name="students", on_delete=models.SET_NULL, null=True)
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
    worker_id = models.UUIDField(unique=True, blank=True)
    cafeteria = models.ForeignKey('restaurants.Cafeteria', related_name="workers", on_delete=models.SET_NULL, null=True, blank=True)
    worker_role = models.CharField(max_length=255, choices=WORKER_ROLES, blank=True)

    def __str__(self):
        return f"{self.user} ({self.worker_role})"

    def save(self, *args, **kwargs):
        if not self.worker_id:
            self.worker_id = uuid.uuid4()
        return super().save(*args, **kwargs)
        
