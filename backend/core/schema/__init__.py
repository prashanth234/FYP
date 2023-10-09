import graphene
from core.schema import userSchema
from core.schema import supportSchema

class CoreQuery(
    userSchema.AuthQuery,
    graphene.ObjectType
):
    pass

class CoreMutation(
    userSchema.AuthMutation,
    supportSchema.Mutation,
    graphene.ObjectType
):
    pass