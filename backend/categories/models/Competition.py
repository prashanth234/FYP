import os
from django.db import models
from django.utils import timezone

from categories.models.Category import *
from core.models.Reward import *
  
class Competition(models.Model):
    def custom_path(instance, filename):
      file_extension = os.path.splitext(filename)[1]
      unique_name = instance.key
      path = f'competitions/{instance.category.key}/'

      # Remove image before creating if image already exists
      file_path = os.path.join(settings.MEDIA_ROOT, f'{path}/{unique_name}{file_extension}')
      if os.path.exists(file_path):
          os.remove(file_path)

      return os.path.join(path, unique_name + file_extension)
       
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    last_date = models.DateField()
    key = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=custom_path, default='')
    points = models.CharField(max_length=255)

    @property
    def is_expired(self):
      kolkata_timezone = timezone.pytz.timezone('Asia/Kolkata')
      current_time_in_kolkata = timezone.now().astimezone(kolkata_timezone)
      return self.last_date <= current_time_in_kolkata.date()

    def __str__(self) -> str:
      return self.name