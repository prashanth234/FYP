import graphene

from categories.schema import categorySchema, competationSchema, postSchema

class Query(
    categorySchema.Query,
    competationSchema.Query,
    postSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    categorySchema.Mutation,
    competationSchema.Mutation,
    postSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)