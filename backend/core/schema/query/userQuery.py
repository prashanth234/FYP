import graphene

# Type
from core.schema.type.UserType import UserType

class UserQuery(graphene.ObjectType):
  user = graphene.Field(UserType)

  def resolve_user(self, info):
    user = info.context.user
    if user.is_authenticated:
        return user
    return None