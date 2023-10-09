import graphene

from categories.schema import categorySchema, competitionSchema, postSchema, likeSchema, winnerSchema

class CategoryQuery(
    categorySchema.Query,
    competitionSchema.Query,
    postSchema.Query,
    likeSchema.Query,
    winnerSchema.Query,
    graphene.ObjectType,
):
    pass

class CategoryMutation(
    # categorySchema.Mutation,
    # competitionSchema.Mutation,
    postSchema.Mutation,
    likeSchema.Mutation,
    graphene.ObjectType
):
    pass