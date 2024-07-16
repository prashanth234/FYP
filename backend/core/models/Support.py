from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from helpers.sendEmail import send_email_to_admins
  
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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
      return self.description
    
@receiver(post_save, sender=Support)
def perform_activity(sender, instance, created, **kwargs):
  if created:
    
    context = {
      'user': instance.user.username,
      'phone': instance.user.email,
      'email': instance.user.phone,
      'description': instance.description
    }

    send_email_to_admins(
      'New Support Request',
      context,
      'support_request.html'
    )