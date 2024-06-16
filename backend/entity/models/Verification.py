from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from helpers.deleteFiles import delete_files
import logging

from entity.models.Entity import Entity
from helpers.sendEmail import send_email_to_admins

logger = logging.getLogger(__name__)

class Verification(models.Model):
    
    # def custom_upload_to(instance, filename):
    #   return custom_upload('internal/verifications', f'user_{instance.user.id}', filename)
    
    REQUEST_CHOICES = (
      ('CREATE', 'Create'),
      ('JOIN', 'Join'),
    )

    STATUS_CHOICES = {
      ('PENDING', 'Pending'),
      ('SUCCESS', 'Success'),
      ('INVAILD', 'Invalid')
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    file = models.FileField()
    request = models.CharField(max_length=100, choices=REQUEST_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
      constraints = [
        models.UniqueConstraint(fields=['entity', 'user', 'request'], name='only_one_unique_validation')
      ]

    def __str__(self) -> str:
      return self.user.username


@receiver(post_save, sender=Verification)
def verification_post_save(sender, instance, created, **kwargs):
  if instance.status == "PENDING":
    context = {
      'user': instance.user.username,
      'request_type': instance.request,
      'entity': instance.entity.name,
      'request_date': instance.updated_at
    }

    send_email_to_admins(
      'New Verification Request',
      context,
      'new_verification_request.html'
    )
  elif not created and instance.status == "SUCCESS":
    if instance.request == 'JOIN' :
      # If verification is succesfull and marked status as success by admin
      logging.info(f'Adding user to entity - Verification: {instance.id}')
      try:
        instance.entity.users.add(instance.user)
        instance.entity.save()
      except Exception as e:
        logging.info(f'Failed to add user to entity - Verification: {instance.id}, error: {str(e)}')
    elif instance.request == 'CREATE':
      # If verification is succesfull and mark entity as public
      logging.info(f'Marking the entity as public - Verification: {instance.id}')
      instance.entity.users.add(instance.user)
      instance.entity.verified = True
      instance.entity.save()

@receiver(post_delete, sender=Verification)
def postfile_post_delete(sender, instance, **kwargs):
    delete_files([instance.file.name])
    logger.info(f'Verification: {instance.id} deleted. Removing the files.')