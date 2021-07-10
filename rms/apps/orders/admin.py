from django.contrib import admin
from . import models

@admin.register(models.Invoice)
class InvoicesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrdersAdmin(admin.ModelAdmin):
    pass
