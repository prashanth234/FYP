from django.db import models
from django.conf import settings
from categories.models.Competition import *
from categories.models.Post import *
from core.models.Reward import *
  
class Winner(models.Model):
    
    POSITION_CHOICES = [(i, str(i)) for i in range(1, 4)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    post = models.OneToOneField(Post, on_delete=models.DO_NOTHING)
    won_by_likes = models.IntegerField()
    position = models.PositiveIntegerField(choices=POSITION_CHOICES)
    points = models.PositiveBigIntegerField()  

    def __str__(self) -> str:
      return self.user.username