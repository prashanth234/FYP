import graphene

from categories.schema import categorySchema, competitionSchema, postSchema, likeSchema, winnerSchema, transactionSchema

class CategoryQuery(
    categorySchema.Query,
    competitionSchema.Query,
    postSchema.Query,
    likeSchema.Query,
    winnerSchema.Query,
    transactionSchema.Query,
    graphene.ObjectType,
):
    pass

class CategoryMutation(
    # categorySchema.Mutation,
    # competitionSchema.Mutation,
    postSchema.Mutation,
    likeSchema.Mutation,
    transactionSchema.Mutation,
    graphene.ObjectType
):
    pass