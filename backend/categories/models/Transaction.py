from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
  
class Transaction(models.Model):
    STATUS_CHOICES = (
        ('Q', 'Pending'),
        ('P', 'Processing'),
        ('S', 'Success'),
        ('F', 'Failed'),
    )

    TYPE_CHOICES = (
       ('UPLOADPOST', 'Upload Post'),
       ('COMPPARTN', 'Competition Participation'),
       ('COMPWINNER', 'Competition Winner'),
       ('SIGNUP', 'SignUp'),
       ('REDEEM', 'Redeem')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Q')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()

    # Examples
    # one transaction belongs to one winner
    # many transactions belongs to one competition
    # many transactions belongs to one category
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
      return self.user.username