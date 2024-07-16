from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
  
class CoinActivity(models.Model):
    STATUS_CHOICES = (
        ('Q', 'Pending'),
        ('S', 'Success'),
        ('F', 'Failed'),
    )

    TYPE_CHOICES = (
       ('PARPTN', 'Participation'),
       ('CPARTN', 'Competition Participation'),
       ('CWINER', 'Competition Winner'),
       ('SIGNUP', 'SignUp'),
       ('REDEEM', 'Redeem')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Q')
    description = models.TextField()
    comments = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    points = models.IntegerField()

    # Examples
    # one coinactivity belongs to one winner
    # many coinactivities belongs to one competition
    # many coinactivities belongs to one category
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
      return self.user.username

@receiver(post_save, sender=CoinActivity)
def perform_activity(sender, instance, created, **kwargs):
  if not created and instance.status == "S":
    instance.user.points += instance.points
    instance.user.save()