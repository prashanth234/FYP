from django.db import models

from categories.models.Category import *
from core.models.Reward import *
from entity.models.Entity  import Entity

from helpers.customUpload import custom_upload
from helpers.common import get_today_date
  
class Competition(models.Model):
    
    def custom_path(instance, filename):
      return custom_upload(f'public/competitions/{instance.category.key}', f'{instance.key}', filename)
       
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    last_date = models.DateField()
    key = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=custom_path, default='')
    points = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True, blank=True)

    @property
    def is_expired(self):
      return self.last_date < get_today_date()

    def __str__(self) -> str:
      return self.name