import graphene
from core.schema import userSchema
from core.schema import supportSchema
from core.schema import coinActivitySchema
from core.schema import rewardSchema
from core.schema import faqSchema

class CoreQuery(
    userSchema.AuthQuery,
    coinActivitySchema.Query,
    rewardSchema.Query,
    faqSchema.Query,
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