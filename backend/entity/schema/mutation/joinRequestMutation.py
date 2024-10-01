import graphene
from graphql import GraphQLError

# Models
from entity.models.Verification import Verification

# Authentication
from graphql_jwt.decorators import login_required

import logging

logger = logging.getLogger(__name__)

class JoinRequestMutation(graphene.Mutation):

  class Arguments:
    # The input arguments for this mutation
    verification_id = graphene.ID(required=True)
    approve = graphene.Boolean(required=True)

  # The class attributes define the response of the mutation
  success = graphene.Boolean()

  @classmethod
  @login_required
  def mutate(cls, root, info, verification_id, approve):

    user = info.context.user

    logger.info(f"User: {user.username} - Requested for to approve: {approve} the verification: {verification_id}.")
    
    try:
      verification = Verification.objects.get(pk=verification_id, status="PENDING")
    except Verification.DoesNotExist:
      raise GraphQLError("Join request not not found.")
    
    verification.status = "SUCCESS" if approve else "INVAILD"
    verification.save()
    
    # TODO: Send the email of the user regrading the status of the request. Currently it is not done because email is not asynchrons.

    logger.info(f"User: {user.username} - Request for approve: {approve} the verification: {verification_id} is successfull.")
    return JoinRequestMutation(success=True)
    
class ApproveJoinRequest(graphene.ObjectType):
  approve_join_request = JoinRequestMutation.Field()