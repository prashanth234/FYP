from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
  
class Like(models.Model):
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # item_type can be either post or comment
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_type', 'item_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item_id',)

    def __str__(self) -> str:
      return self.user