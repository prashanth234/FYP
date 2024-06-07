from django.db import models
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from categories.models.Competition import *
from post.models.Post import *

from core.models.CoinActivity import *
  
class Winner(models.Model):
    
    POSITION_CHOICES = [(i, str(i)) for i in range(1, 4)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    post = models.OneToOneField(Post, on_delete=models.DO_NOTHING)
    won_by_likes = models.IntegerField()
    position = models.PositiveIntegerField(choices=POSITION_CHOICES)
    points = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
      return self.user.username
    

@receiver(pre_save, sender=Winner)
def perform_activity(sender, instance, **kwargs):
  if not instance.id:
    instance.user = instance.post.user
    instance.competition = instance.post.competition

@receiver(post_save, sender=Winner)
@transaction.atomic
def perform_activity(sender, instance, created, **kwargs):
  if created:
    description = f'{instance.competition.name} Contest - Winner {instance.position} Reward'
    coinactivity = CoinActivity(type='CWINER', user=instance.user, points=instance.points, description=description, content_object=instance, status='S')
    instance.user.points += instance.points
    instance.user.save()
    coinactivity.save()