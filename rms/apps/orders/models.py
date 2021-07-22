from django.db import models
from django.contrib.auth import get_user_model

class PurchaseOrder(models.Model):
    """Model for managing orders at a restaurant"""

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed',  'Closed Completed'),
    )

    DELIVERY_MODE = (
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    )

    order_id = models.UUIDField(unique=True)
    cafeteria = models.ForeignKey('restaurants.Cafeteria', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Student', related_name="orders", on_delete=models.CASCADE)
    approved_by_worker = models.ForeignKey('accounts.Worker', related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    delivery_mode = models.CharField(max_length=255, choices=DELIVERY_MODE)
    delivery_date = models.DateTimeField(blank=True)
    delivery_address = models.TextField()
    notes = models.TextField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    class Meta:
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"ORDER NO: #{self.order_id}"

class PurchaseLine(models.Model):
    """Model for managing purchase order items"""

    order = models.ForeignKey('orders.PurchaseOrder', related_name="lines", on_delete=models.CASCADE)
    menu = models.ForeignKey('restaurants.Menu', related_name="purchase_lines", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_ready = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=5)


    def __str__(self):
        return self.menu.name

class Invoice(models.Model):
    """Model for managing invoices issued to users"""

    invoice_id = models.UUIDField(unique=True)
    order = models.ForeignKey('orders.PurchaseOrder', on_delete=models.CASCADE)
    cafeteria = models.ForeignKey('restaurants.Cafeteria', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"INVOICE NO: #{self.invoice_id}"
