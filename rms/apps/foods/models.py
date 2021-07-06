from django.db import models

class FoodCategory(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Name of food")
    description = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    photo = models.ImageField(verbose_name="Photo", upload_to="photos/")
    price = models.DecimalField(decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

