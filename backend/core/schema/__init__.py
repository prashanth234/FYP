import graphene
from core.schema import userSchema
from core.schema import supportSchema
from core.schema import transactionSchema

class CoreQuery(
    userSchema.AuthQuery,
    transactionSchema.Query,
    graphene.ObjectType
):
    pass

class CoreMutation(
    userSchema.AuthMutation,
    supportSchema.Mutation,
    transactionSchema.Mutation,
    graphene.ObjectType
):
    pass