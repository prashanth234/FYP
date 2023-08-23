from django.db import models
from django.conf import settings
from categories.models.Competition import *
from categories.models.Post import *
  
class Winner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    likes = models.IntegerField()

    def __str__(self) -> str:
      return self.user