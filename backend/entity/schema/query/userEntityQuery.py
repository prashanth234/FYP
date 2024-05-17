import graphene

from entity.models.Verification import Verification

# Authentications
from graphql_jwt.decorators import login_required

import logging

logger = logging.getLogger(__name__)

class ResponseType(graphene.ObjectType):
  status = graphene.String()

class UserEntityCheck(graphene.ObjectType):
   
  user_entity_check = graphene.Field(
    ResponseType,
    entity_id=graphene.String()
  )

  @classmethod
  def get_status(cls, user, entity_id):
    status = 'NOTFOUND'

    if not user.is_authenticated:
      return status

    # Check if user exists in the entity 
    if user.user_of_entities.filter(pk=entity_id).exists():
      status = 'SUCCESS'
    else:
      try:
        # Check if verification is pending
        verfication = Verification.objects.get(user=user, entity_id=entity_id)
        status = verfication.status
      except Verification.DoesNotExist:
        pass

    return status

  def resolve_user_entity_check(self, info, entity_id):

    user = info.context.user
    logger.info(f"User: {user.username} - requested for user check for entity {entity_id}")
    status = self.get_status(user, entity_id)
    logger.info(f"User: {user.username} - requested for user check for entity {entity_id} - Status {status}")

    return ResponseType(status=status)