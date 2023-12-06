from django.db import models
from django.conf import settings
  
class Support(models.Model):
    
    STATUS_CHOICES = (
      ('P', 'Pending'),
      ('R', 'Resolved'),
    )
    
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    comments = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
      return self.description