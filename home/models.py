from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Profile(models.Model):

    mobile = models.IntegerField(unique=True)
    address = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["user"]

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})


class Advertisement(models.Model):

    COLOR_CHOICES = (
        ("green", "GREEN"),
        ("blue", "BLUE"),
        ("red", "RED"),
        ("orange", "ORANGE"),
        ("black", "BLACK"),
    )

    title = models.CharField(max_length=50)
    house_address = models.TextField(max_length=255)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    house_type = models.CharField(max_length=6, choices=COLOR_CHOICES, default="green")
    rent_fee = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(10000), MaxValueValidator(100000)]
    )
    image = models.ImageField(
        upload_to="images/", height_field=None, width_field=None, max_length=None
    )
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Advertisement_detail", kwargs={"pk": self.pk})


class Images(models.Model):
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name="images"
    )
    images = models.FileField(upload_to="images/")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.advertisement.title




class Favourite(models.Model):

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    favourite_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favourite"
        verbose_name_plural = "Favourites"

    def __str__(self):
        return self.advertisement.title

    def get_absolute_url(self):
        return reverse("Favourite_detail", kwargs={"pk": self.pk})
