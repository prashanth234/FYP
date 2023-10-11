import graphene
from core.schema import userSchema
from core.schema import supportSchema
from core.schema import coinActivitySchema
from core.schema import rewardSchema

class CoreQuery(
    userSchema.AuthQuery,
    coinActivitySchema.Query,
    rewardSchema.Query,
    graphene.ObjectType
):
    pass

class CoreMutation(
    userSchema.AuthMutation,
    supportSchema.Mutation,
    coinActivitySchema.Mutation,
    graphene.ObjectType
):
    pass