from django.db import models
from django.conf import settings
  
class Redeem(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('R', 'Redeemed'),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()

    def __str__(self) -> str:
      return self.user