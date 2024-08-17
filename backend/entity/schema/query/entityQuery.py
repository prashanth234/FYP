import graphene

from entity.schema.type.EntityType import EntityType
from entity.models.Entity import Entity

from core.schema.type.UserType import UserType

class Entities(graphene.ObjectType):

  entities = graphene.List(EntityType)

  def resolve_entities(root, info):
    return Entity.objects.filter(verified=True)
  
class EntityDetails(graphene.ObjectType):

  entity_details = graphene.Field(
    EntityType,
    id=graphene.ID(required=True)
  )

  def resolve_entity_details(root, info, id):
    return Entity.objects.get(pk=id, verified=True)
  
class EntityUsers(graphene.ObjectType):

  entity_users = graphene.List(UserType, id=graphene.ID(required=True))

  def resolve_entity_users(root, info, id):
    entity = Entity.objects.get(pk=id, verified=True)
    return entity.users.all()



  