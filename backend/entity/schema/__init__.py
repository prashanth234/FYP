import graphene

from entity.schema.query.entityQuery import Entities, EntityDetails, EntityUsers
from entity.schema.query.entityPostsQuery import EntityPosts
from entity.schema.query.userEntityQuery import UserEntityCheck
from entity.schema.query.joinRequestsQuery import JoinRequests

from entity.schema.mutation.joinEntityMutation import JoinEntity
from entity.schema.mutation.createEntityMutation import CreateEntity
from entity.schema.mutation.editEntityMutation import EditEntity
from entity.schema.mutation.joinRequestMutation import ApproveJoinRequest

class EntityQuery(
    Entities,
    EntityDetails,
    EntityPosts,
    EntityUsers,
    UserEntityCheck,
    JoinRequests,
    graphene.ObjectType,
):
    pass

class EntityMutation(
    JoinEntity,
    CreateEntity,
    EditEntity,
    ApproveJoinRequest,
    graphene.ObjectType
):
    pass