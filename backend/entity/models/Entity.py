from django.db import models
from django.conf import settings
from helpers.customUpload import custom_upload
from django.dispatch import receiver
from django.db.models.signals import post_delete
from helpers.deleteFiles import delete_files
from django.utils.translation import gettext_lazy as _
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Entity(models.Model):

    def custom_upload_to(instance, filename):
      newfilename = f"entity_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
      return custom_upload('public/entities', newfilename, filename)

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
    # if True: Users need to create a verification request to entity admin
    verify_users = models.BooleanField(default=False)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_of_entities', blank=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_of_entities', blank=True)

    city = models.TextField(null=True, blank=True)    
    phone = models.CharField(max_length=150, null=True, blank=True, unique=True)
    email = models.CharField(max_length=150, null=True, blank=True, unique=True)

    linkedin = models.TextField(max_length=300, null=True, blank=True)
    facebook = models.TextField(max_length=300, null=True, blank=True)
    instagram = models.TextField(max_length=300, null=True, blank=True)
    maps = models.TextField(max_length=300, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
      return self.name

@receiver(post_delete, sender=Entity)
def entity_post_delete(sender, instance, **kwargs):
    delete_files([instance.image.name])
    logger.info(f'Entity: {instance.id} deleted. Removing the files.')