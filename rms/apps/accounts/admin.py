from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('avatar', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_matric', 'student_gender', 'student_level')


@admin.register(models.Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass
