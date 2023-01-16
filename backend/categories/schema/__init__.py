import graphene

from categories.schema import categorySchema

class Query(
    categorySchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    categorySchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)