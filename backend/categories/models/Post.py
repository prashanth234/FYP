from django.db import models
from django.conf import settings

from categories.models.Category import *
from categories.models.Competition import *

class Post(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self) -> str:
      return self.description
    
class PostFile(models.Model):
    file = models.FileField(upload_to="files")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)