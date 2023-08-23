import graphene

from categories.schema import categorySchema, competitionSchema, postSchema, likeSchema, redeemSchema, winnerSchema

class CategoryQuery(
    categorySchema.Query,
    competitionSchema.Query,
    postSchema.Query,
    likeSchema.Query,
    redeemSchema.Query,
    winnerSchema.Query,
    graphene.ObjectType
):
    pass

class CategoryMutation(
    # categorySchema.Mutation,
    # competitionSchema.Mutation,
    postSchema.Mutation,
    likeSchema.Mutation,
    redeemSchema.Mutation,
    graphene.ObjectType
):
    pass