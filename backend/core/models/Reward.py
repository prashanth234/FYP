from django.db import models
from django.conf import settings

from helpers.customUpload import custom_upload

class Reward(models.Model):

	def custom_upload_to(instance, filename):
		return custom_upload(f'public/rewards', f'{instance.type}', filename)

	TYPE_CHOICES = (
		('ZOMATO', 'Zomato'),
		('SWIGGY', 'Swiggy'),
		('BMS', 'Book My Show'),
		('AMAZON', 'Amazon'),
		('FLIPKRT', 'Flipkart'),
		('MYNTRA', 'Myntra'),
		('AJIO', 'Ajio')
	)

	name = models.CharField(max_length=255)
	image = models.ImageField(upload_to=custom_upload_to)
	points = models.CharField(max_length=255)
	pointsvalue = models.PositiveIntegerField(null=True, blank=True)
	type = models.CharField(max_length=100, choices=TYPE_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
			return self.name

