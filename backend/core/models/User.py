from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.CoinActivity import CoinActivity

class User (AbstractUser):
  GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
  
  email = models.EmailField(max_length=150, blank=True, null=True, unique=True)
  phone = models.CharField(unique=True, max_length=15, null=True, blank=True)
  avatar = models.FileField(upload_to="users", blank=True, null=True)  
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  points = models.IntegerField(default=settings.USER_SIGNUP_POINTS)

  USERNAME_FIELD = "username"
  EMAIL_FIELD = "email"

  def save(self, *args, **kwargs):
    if self.email == '':
      self.email = None
    super(User, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def perform_activity(sender, instance, created, **kwargs):
  if created:
    coinactivity = CoinActivity(type='SIGNUP', user=instance, points=settings.USER_SIGNUP_POINTS, description='Welcome Reward', status='S')
    coinactivity.save()