from django.db import models
from django.contrib.auth import get_user_model

class PurchaseOrder(models.Model):
    """Model for managing orders at a restaurant"""

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed',  'Closed Completed'),
    )

    order_id = models.UUIDField(primary_key=True)
    supplier = models.ForeignKey('restaurants.Cafeteria', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(blank=True)
    delivery_address = models.TextField()
    requested_by = models.ForeignKey('accounts.Student', related_name="orders", on_delete=models.CASCADE)
    approved_by = models.ForeignKey('accounts.Worker', related_name="orders", on_delete=models.CASCADE)
    notes = models.TextField()
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    total_price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"ORDER NO: #{self.order_id}"


class PurchaseItem(models.Model):
    """Model for managing purchase order items"""

    order = models.ForeignKey('orders.PurchaseOrder', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_code = models.UUIDField()
    item_quantity = models.IntegerField()
    item_price = models.DecimalField(decimal_places=2, max_digits=5)
    item_discount = models.DecimalField(decimal_places=2, max_digits=5)
    total_price = models.DecimalField(decimal_places=2, max_digits=5)


    def __str__(self):
        return self.item_name


class Invoice(models.Model):
    """Model for managing invoices issued to users"""

    purchase_order = models.ForeignKey('orders.PurchaseOrder', on_delete=models.CASCADE)
    purchaser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vendor = models.ForeignKey('restaurants.Cafeteria', on_delete=models.CASCADE)
    invoice_id = models.UUIDField(primary_key=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    reference_id = models.CharField(max_length=255)

    def __str__(self):
        return f"INVOICE NO: #{self.invoice_id}"
