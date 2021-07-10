from django.contrib import admin
from django.contrib.admin.options import TabularInline
from . import models

@admin.register(models.Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    pass


class Reviews(admin.TabularInline):
    model = models.Review


@admin.register(models.CafeteriaMenu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [
        Reviews
    ]
