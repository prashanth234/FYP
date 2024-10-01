import graphene
from graphql import GraphQLError

from entity.schema.type.JoinRequestType import JoinRequestType
from entity.models.Verification import Verification

# Authentications
from graphql_jwt.decorators import login_required
from entity.schema.query.userEntityQuery import UserEntityCheck

import logging

logger = logging.getLogger(__name__)

class JoinRequests(graphene.ObjectType):

  join_requests = graphene.List(JoinRequestType, entity_id=graphene.ID(required=True))

  @login_required
  def resolve_join_requests(root, info, entity_id):

    logger.info(f"User: {info.context.user.username} - Requested for entity: {entity_id} join verifications.")

    if not UserEntityCheck.has_access(info.context.user, entity_id, True):
      logger.info(f"User: {info.context.user.username} - tried to fetch entity: {entity_id} verification. Rejecting the request!!!!")
      return GraphQLError("Unauthorized Action!!!")

    return Verification.objects.filter(entity_id=entity_id, request="JOIN", status="PENDING")