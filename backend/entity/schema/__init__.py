import graphene

from entity.schema.entityQuery import Entities, EntityDetails
from entity.schema.entityPostsQuery import EntityPosts

class EntityQuery(
    Entities,
    EntityDetails,
    EntityPosts,
    graphene.ObjectType,
):
    pass

# class EntityMutation(
#     entitySchema.Mutation,
#     graphene.ObjectType
# ):
#     pass