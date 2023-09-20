from django.db import models
from django.conf import settings
from categories.models.Competition import *
from categories.models.Post import *
from categories.models.Reward import *
  
class Winner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING)
    post = models.OneToOneField(Post, on_delete=models.DO_NOTHING)
    won_by_likes = models.IntegerField()
    reward = models.ForeignKey(Reward, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
      return self.user.username