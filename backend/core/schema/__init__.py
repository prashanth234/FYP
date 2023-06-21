import graphene
from core.schema import userSchema

class CoreQuery(
    userSchema.AuthQuery,
    graphene.ObjectType
):
    pass

class CoreMutation(
    userSchema.AuthMutation,
    graphene.ObjectType
):
    pass