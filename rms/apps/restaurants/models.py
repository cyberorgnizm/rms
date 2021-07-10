from django.db import models
from django.contrib.auth import get_user_model

class Cafeteria(models.Model):
    """Model for managing cafeterias within college campus"""

    cafeteria_name = models.CharField(max_length=255)
    cafeteria_email = models.EmailField(blank=True, null=True)
    cafeteria_image = models.ImageField(upload_to="cafeterias")
    cafeteria_manager = models.ForeignKey('accounts.Worker', on_delete=models.SET_NULL, null=True)
    cafeteria_address = models.TextField()
    cafeteria_work_hours = models.DurationField()

    def __str__(self):
        return self.cafeteria_name

class CafeteriaMenu(models.Model):
    """Model for managing menus available at campus cafeterias"""

    MENU_TYPES = (
        ('food', 'Food'), 
        ('drink', 'Drink'),
        ('snack', 'Snack'),
    )

    cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=255)
    menu_image = models.ImageField(upload_to="products")
    menu_description = models.TextField()
    menu_slug = models.SlugField(blank=True, unique=True)
    menu_type = models.CharField(max_length=255, choices=MENU_TYPES)
    menu_price = models.DecimalField(decimal_places=2, max_digits=5)
    menu_discount = models.DecimalField(decimal_places=2, default=0.00, max_digits=5)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Menus"


class Review(models.Model):
    """Model for managing reviews on cafeterias menus"""

    reviewer = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    review_id = models.UUIDField(primary_key=True)
    review_menu = models.ForeignKey('CafeteriaMenu', on_delete=models.CASCADE)
    review_ratings = models.DecimalField(decimal_places=1, max_digits=5)
    review_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"REVIEW NO: #{self.review_id}"
