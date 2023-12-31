import os
from django.db import models
from django.conf import settings

class Reward(models.Model):
  
	def custom_upload_to(instance, filename):
		"""
		Custom upload_to function to generate image file names.
		"""
		# Get the original file extension
		file_extension = os.path.splitext(filename)[1]

		# Generate a unique file name based on the instance's field
		unique_name = instance.type

		# Remove image before creating if image already exists
		file_path = os.path.join(settings.MEDIA_ROOT, f'rewards/{unique_name}{file_extension}')
		if os.path.exists(file_path):
				os.remove(file_path)

		# Return the custom file path.
		return os.path.join('rewards/', unique_name + file_extension)

	TYPE_CHOICES = (
		('ZOMATO', 'Zomato'),
		('SWIGGY', 'Swiggy'),
		('BMS', 'Book My Show'),
		('AMAZON', 'Amazon'),
		('FLIPKART', 'Flipkart'),
		('MYNTRA', 'Myntra'),
		('AJIO', 'Ajio')
	)

	name = models.CharField(max_length=255)
	image = models.ImageField(upload_to=custom_upload_to)
	points = models.CharField(max_length=255)
	pointsvalue = models.PositiveIntegerField(null=True, blank=True)
	type = models.CharField(max_length=100, choices=TYPE_CHOICES)

	def __str__(self) -> str:
			return self.name

