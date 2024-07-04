from django.db import models
from django.contrib.auth.models import User

class CustomUserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()

    # Additional custom fields
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'