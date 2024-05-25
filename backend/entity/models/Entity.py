from django.db import models
from django.conf import settings
from helpers.custom_upload import custom_upload
from django.utils.translation import gettext_lazy as _

class Entity(models.Model):

    def custom_upload_to(instance, filename):
      return custom_upload('public/entities', f'entity_{instance.id}', filename)

    # Also update in UI
    TYPE_CHOICES = (
		  ('School', 'School'),
		  ('College', 'College'),
      ('Institute', 'Institute'),
      ('Others', 'Others'),
	  )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    other_type = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=custom_upload_to, default='', null=True, blank=True)
    ispublic = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_of_entities', blank=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_of_entities')

    city = models.TextField(null=True, blank=True)    
    phone = models.CharField(max_length=150, null=True, blank=True, unique=True)
    email = models.CharField(max_length=150, null=True, blank=True, unique=True)

    linkedin = models.TextField(max_length=300, null=True, blank=True)
    facebook = models.TextField(max_length=300, null=True, blank=True)
    instagram = models.TextField(max_length=300, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.name