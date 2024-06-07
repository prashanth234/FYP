from django.db import models
from django.utils import timezone
import zoneinfo

from categories.models.Category import *
from core.models.Reward import *

from helpers.customUpload import custom_upload
  
class Competition(models.Model):
    
    def custom_path(instance, filename):
      return custom_upload(f'public/competitions/{instance.category.key}', f'{instance.key}', filename)
       
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    last_date = models.DateField()
    key = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=custom_path, default='')
    points = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True, blank=True)

    @property
    def is_expired(self):
      kolkata_timezone = zoneinfo.ZoneInfo('Asia/Kolkata')
      current_time_in_kolkata = timezone.now().astimezone(kolkata_timezone)
      return self.last_date <= current_time_in_kolkata.date()

    def __str__(self) -> str:
      return self.name