import graphene
from core.schema import CoreQuery, CoreMutation
from categories.schema import CategoryQuery, CategoryMutation
from post.schema import PostQuery, PostMutation
# from entity.schema import EntityQuery

class Query(
    CoreQuery,
    CategoryQuery,
    PostQuery,
    # EntityQuery,
    graphene.ObjectType
):
    pass

class Mutation(
    CoreMutation,
    CategoryMutation,
    PostMutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)