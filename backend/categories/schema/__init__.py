import graphene

from categories.schema import categorySchema, competitionSchema, postSchema

class Query(
    categorySchema.Query,
    competitionSchema.Query,
    postSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    categorySchema.Mutation,
    competitionSchema.Mutation,
    postSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)