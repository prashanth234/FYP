import graphene
from graphql import GraphQLError
from core.models.User import User

class UserAvailableQuery(graphene.ObjectType):

  user_available = graphene.Boolean(
    email=graphene.String(),
    phone=graphene.String()
  )
  
  def resolve_user_available(cls, info, email=None, phone=None):

    if email == None and phone == None:
      raise GraphQLError("Please provide either phone or email")

    try:
      if email:
          User.objects.get(email=email)
      else:
          User.objects.get(phone=phone)
    except User.DoesNotExist:
      return False

    return True