from django.dispatch import receiver
from django.conf import settings

from core.models.CoinActivity import CoinActivity
from entity.models.Entity import Entity
from authentication.signals import user_verified
import logging

logger = logging.getLogger(__name__)

# When a user is verified.
@receiver(user_verified)
def perform_activity(sender, user, **kwargs):

  try:

    # Create coin activity
    coinactivity = CoinActivity(type='SIGNUP', user=user, points=settings.USER_SIGNUP_POINTS, description='Welcome Reward', status='S')
    coinactivity.save()

    # Add user to selfdive entity
    entity = Entity.objects.get(pk=1)
    entity.users.add(user)
    entity.save()

    logger.info(f"User: {user.username} - got verified")

  except Exception as e:
    logger.error(f"User: {user.username} - verification failed due to {str(e)}")
