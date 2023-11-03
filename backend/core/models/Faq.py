from django.db import models
from django.conf import settings
  
class Faq(models.Model):
    
    TYPE_CHOICES = (
      ('REWARD', 'Reward'),
    )

    question = models.TextField()
    answer = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    order = models.PositiveIntegerField()

    def __str__(self) -> str:
      return self.question