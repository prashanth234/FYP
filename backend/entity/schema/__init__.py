import graphene

from entity.schema.query.entityQuery import Entities, EntityDetails
from entity.schema.query.entityPostsQuery import EntityPosts
from entity.schema.query.userEntityQuery import UserEntityCheck

from entity.schema.mutation.joinEntityMutation import JoinEntity
from entity.schema.mutation.createEntityMutation import CreateEntity
from entity.schema.mutation.editEntityMutation import EditEntity

class EntityQuery(
    Entities,
    EntityDetails,
    EntityPosts,
    UserEntityCheck,
    graphene.ObjectType,
):
    pass

class EntityMutation(
    JoinEntity,
    CreateEntity,
    EditEntity,
    graphene.ObjectType
):
    pass