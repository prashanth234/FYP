from django.db import models
from django.conf import settings
import os  

class Entity(models.Model):
    
    def custom_upload_to(instance, filename):
        """
        Custom upload_to function to generate image file names.
        """
        # Get the original file extension
        file_extension = os.path.splitext(filename)[1]

        # Generate a unique file name based on the instance's field
        unique_name = instance.key

        # Remove image before creating if image already exists
        file_path = os.path.join(settings.MEDIA_ROOT, f'entities/{unique_name}{file_extension}')
        if os.path.exists(file_path):
            os.remove(file_path)

        # Return the custom file path
        return os.path.join('entities/', unique_name + file_extension)
    
    TYPE_CHOICES = (
		('SCHOOL', 'School'),
		('COLLEGE', 'College'),
        ('OTHERS', 'Others'),
	)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    type_name = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=custom_upload_to, default='', null=True, blank=True)

    city = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=150, null=True, blank=True, unique=True)
    email = models.CharField(max_length=150, null=True, blank=True, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.name
    

# Name
# location
# image
# contact
# socail links
# followers

# Art (count)