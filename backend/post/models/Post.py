from django.db import models
from django.conf import settings

from categories.models.Category import *
from categories.models.Competition import *

from entity.models.Entity import Entity

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from post.tasks.deleteImages import delete_images

import logging

logger = logging.getLogger(__name__)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    is_bot = models.BooleanField(default=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    ispublic = models.BooleanField(default=True)
    
    def __str__(self) -> str:
      return self.description[:25] if self.description else str(self.id)
    
class PostFile(models.Model):
    file = models.FileField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=PostFile)
def postfile_post_save(sender, instance, created, **kwargs):
    context = getattr(instance, '_context', None)
    if not created and context:
        logger.info(f'Post file: {instance.id} of the post: {instance.post.id} udpated. Removing the old files: {context}')
        delete_images(context["file"])

@receiver(post_delete, sender=PostFile)
def postfile_post_delete(sender, instance, **kwargs):
    path = instance.file.name
    logger.info(f'Post file: {instance.id} of the post: {instance.post.id} deleted. Removing the old files: {path}')
    delete_images(path)