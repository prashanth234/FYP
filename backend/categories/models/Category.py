import os
from django.db import models
  
class Category(models.Model):

    def custom_upload_to(instance, filename):
        """
        Custom upload_to function to generate image file names.
        """
        # Get the original file extension
        file_extension = os.path.splitext(filename)[1]

        # Generate a unique file name based on the instance's field
        unique_name = instance.type

        # Return the custom file path
        return os.path.join('categories/', unique_name + file_extension)
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to=custom_upload_to, default='')

    def __str__(self) -> str:
      return self.name