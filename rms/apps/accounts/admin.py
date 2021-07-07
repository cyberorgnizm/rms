from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.contrib.auth import get_user_model
from . import models


@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    pass


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass
