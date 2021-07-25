from django.contrib import admin
from . import models

@admin.register(models.Invoice)
class InvoicesAdmin(admin.ModelAdmin):
    pass


class PurchaseLineTabularAdmin(admin.TabularInline):
    model = models.PurchaseLine
    extra = 0


@admin.register(models.PurchaseOrder)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [PurchaseLineTabularAdmin]
