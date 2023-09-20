from django.db import models

class Reward(models.Model):

  TYPE_CHOICES = (
      ('COMPETITION', 'Competition'),
  )

  points = models.PositiveIntegerField()
  position = models.PositiveIntegerField()
  type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="COMPETITION")

  def __str__(self) -> str:
      return f'pos-{self.position}-pts-{self.points}'

