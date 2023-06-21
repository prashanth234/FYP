import graphene
from core.schema import CoreQuery, CoreMutation
from categories.schema import CategoryQuery, CategoryMutation

class Query(
    CoreQuery,
    CategoryQuery,
    graphene.ObjectType
):
    pass

class Mutation(
    CoreMutation,
    CategoryMutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)