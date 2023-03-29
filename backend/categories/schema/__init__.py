import graphene

from categories.schema import categorySchema, competitionSchema, postSchema, likeSchema

class Query(
    categorySchema.Query,
    competitionSchema.Query,
    postSchema.Query,
    likeSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    categorySchema.Mutation,
    competitionSchema.Mutation,
    postSchema.Mutation,
    likeSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)