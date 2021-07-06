from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.contrib.auth import get_user_model

@admin.register(get_user_model())
class UserAdmin(AbstractUserAdmin):
    pass