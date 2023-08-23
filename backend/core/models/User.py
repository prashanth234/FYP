from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
  GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
  
  email = models.EmailField(unique=True)
  avatar = models.FileField(upload_to="users", blank=True, null=True)  
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  points = models.IntegerField(default=200)

  USERNAME_FIELD = "username"
  EMAIL_FIELD = "email"