from django.db import models
from django.conf import settings

from categories.models.Category import *
from categories.models.Competition import *

from entity.models.Entity import Entity

import os

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    is_bot = models.BooleanField(default=False)
    
    def __str__(self) -> str:
      return self.description
    
class PostFile(models.Model):
    file = models.FileField(upload_to="posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_path(self):
        # Assuming 'image_field' is the name of your ImageField
        if self.file:
            return os.path.join(settings.MEDIA_ROOT, str(self.file))
        return None