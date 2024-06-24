from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField(blank=True, default="", verbose_name="Image URL")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.starting_bid})"
