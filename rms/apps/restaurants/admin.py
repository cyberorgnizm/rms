from django.contrib import admin
from . import models

class CafeteriaReviewTabularAdmin(admin.TabularInline):
    model = models.CafeteriaReview
    extra = 0


@admin.register(models.Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('name', 'email', 'opening_hour', 'closing_hour')

    inlines = [
        CafeteriaReviewTabularAdmin
    ]

    def image_tag(self, obj):
        """Image preview in Django Admin"""
        from django.utils.html import format_html
        return format_html('<img src="{}" height=150 width=200 style="border-radius: 10px" />'.format(obj.cafeteria_image.url))
    
    image_tag.short_description = 'Photo'


class MenuReviewTabularAdmin(admin.TabularInline):
    model = models.MenuReview
    extra = 0


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_type', 'price', 'cafeteria')
    inlines = [
        MenuReviewTabularAdmin
    ]
