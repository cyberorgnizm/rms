from django.db import models
from django.utils.text import slugify
from django.conf import settings


RATING_CHOICES = (
    (1, 'terrible'),
    (2, 'poor'),
    (3, 'good'),
    (4, 'very good'),
    (5, 'excellent')
)

class Cafeteria(models.Model):
    """Model for managing cafeterias within college campus"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to=f"{settings.MEDIA_ROOT}cafeterias")
    manager = models.ForeignKey('accounts.Worker', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    opening_hour = models.TimeField(blank=True, null=True)
    closing_hour = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class CafeteriaReview(models.Model):
    """Model for managing reviews on cafeterias"""

    cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"REVIEW NO: #{self.id}"


class Menu(models.Model):
    """Model for managing menus available at campus cafeterias"""

    MENU_TYPES = (
        ('food', 'Food'), 
        ('drink', 'Drink'),
        ('snack', 'Snack'),
    )

    cafeteria = models.ForeignKey('Cafeteria', related_name="menus", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f"{settings.MEDIA_ROOT}products")
    description = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    menu_type = models.CharField(max_length=255, choices=MENU_TYPES)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Menus"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class MenuReview(models.Model):
    """Model for managing reviews on cafeterias menus"""

    reviewer = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"REVIEW NO: #{self.id}"
