import graphene

from categories.schema import categorySchema, competationSchema

class Query(
    categorySchema.Query,
    competationSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    categorySchema.Mutation,
    competationSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)