from graphql_auth import mutations
from graphql import GraphQLError
import graphene
from core.models.User import User
from entity.models.Entity import Entity
from entity.schema.query.userEntityQuery import UserEntityCheck
from django.utils.translation import gettext as _

class CustomVerifyToken(mutations.VerifyToken):

  class Arguments:
    token = graphene.String()
    entity = graphene.String()

  @classmethod
  def mutate(cls, root, info, entity=None, **kwargs):
    # Call the original verify token logic
    result = super().mutate(root, info, **kwargs)

    if result.success and entity:
      try:
        entity = Entity.objects.get(key=entity, ispublic=True)
      except Entity.DoesNotExist:
        return cls(success=False, errors={"message": _("entity doesn't exist."), "code": "entity_not_found"})
      
      try:
        user = User.objects.get(username=result.payload['username'])
      except:
        return cls(success=False, errors={"message": _("user doesn't exist"), "code": "access_denied"})

      if not UserEntityCheck.has_access(user=user, entity_id=entity.id):
        return cls(success=False, errors={"message": _("no access"), "code": "access_denied"})

    return result