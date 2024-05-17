from django.db import models
from django.conf import settings
from helpers.custom_upload import custom_upload
  
class Category(models.Model):

    def custom_upload_to(instance, filename):
      return custom_upload('public/categories', f'{instance.key}', filename)

    TYPE_CHOICES = (
        ('TEXT', 'Text'),
        ('IMAGETEXT', 'Image and Text'),
        ('IMAGE', 'Image'),
    )
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    key = models.CharField(max_length=100, unique=True)
    oftype = models.CharField(max_length=100, choices=TYPE_CHOICES, default="IMAGETEXT")
    image = models.ImageField(upload_to=custom_upload_to, default='')
    order = models.PositiveIntegerField(default=0)
    hide = models.BooleanField(default=False)
    color = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
      return self.name