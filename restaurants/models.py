from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    cuisine_type = models.CharField(max_length=100)
    meal_name = models.CharField(max_length=100, default="Signature Meal")
    description = models.TextField(default="A delicious signature dish.")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(default="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=500")
    logo_url = models.URLField(default="https://cdn-icons-png.flaticon.com/512/1996/1996055.png")
    is_veg = models.BooleanField(default=True)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.name
