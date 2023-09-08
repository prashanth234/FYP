import os
from django.db import models
from categories.models.Category import *
  
class Competition(models.Model):
    def custom_path(instance, filename):
      file_extension = os.path.splitext(filename)[1]
      unique_name = instance.name
      path = f'competitions/{instance.category.key}/'

      return os.path.join(path, unique_name + file_extension)
       
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    last_date = models.DateField()
    points = models.IntegerField()
    image = models.ImageField(upload_to=custom_path, default='')

    def __str__(self) -> str:
      return self.name