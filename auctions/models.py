from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    ELECTRONICS = "E"
    FASHION = "F"
    HOME = "H"
    TOYS = "T"
    CATEGORY_CHOICES = {
        ELECTRONICS: "Electronics",
        FASHION: "Fashion",
        HOME: "Home",
        TOYS: "Toys",
    }

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField(blank=True, default="", verbose_name="Image URL")
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default=ELECTRONICS,
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings", null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.starting_bid})"
