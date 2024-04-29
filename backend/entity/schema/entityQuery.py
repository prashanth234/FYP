import graphene
from graphql import GraphQLError

from entity.schema.type.EntityType import EntityType
from entity.models.Entity import Entity

class Entities(graphene.ObjectType):

  entities = graphene.List(EntityType)

  def resolve_entities(root, info):
    return Entity.objects.all()
  
class EntityDetails(graphene.ObjectType):

  entity_details = graphene.Field(
      EntityType,
      id=graphene.ID(required=True)
  )

  def resolve_entity_details(root, info, id):
      return Entity.objects.get(pk=id)


  