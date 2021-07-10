from django.contrib import admin
from . import models

@admin.register(models.Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """Image preview in Django Admin"""
        from django.utils.html import format_html
        return format_html('<img src="{}" height=150 width=200 style="border-radius: 10px" />'.format(obj.cafeteria_image.url))
    
    image_tag.short_description = 'Photo'


class Reviews(admin.TabularInline):
    model = models.Review


@admin.register(models.CafeteriaMenu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [
        Reviews
    ]
