from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.
class Registration(models.Model):
    
    username = models.CharField( max_length=50)
    email = models.EmailField( max_length=50)
    password = models.CharField(max_length = 50)
    mobile = models.IntegerField(unique=True)
    address = models.TextField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add=True)
    # advertisements = models.ForeignKey('Advertisement', on_delete=models.PROTECT,default= None, null = True, )

    class Meta:
        verbose_name = ("Registration")
        verbose_name_plural = ("Registrations")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("Registration_detail", kwargs={"pk": self.pk})




class Advertisement(models.Model):

    COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
    )

    owner = models.ForeignKey(Registration, on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    house_type = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')
    house_address = models.TextField(max_length = 255)
    rent_fee =models.PositiveIntegerField(default=10, validators=[MinValueValidator(5000), MaxValueValidator(100000)])
    image = models.ImageField( upload_to='images/', height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = ("Advertisement")
        verbose_name_plural = ("Advertisements")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Advertisement_detail", kwargs={"pk": self.pk})


class Images(models.Model):
    advertisement = models.ForeignKey(Advertisement, default=None, on_delete=models.CASCADE, related_name='+')
    images = models.FileField(upload_to = 'images/')

    class Meta:
        verbose_name = ("Image")
        verbose_name_plural = ("Images")

    def __str__(self):
        return self.advertisement.title  
