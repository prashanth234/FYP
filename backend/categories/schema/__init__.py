import graphene

from categories.schema import categorySchema, competitionSchema, winnerSchema

class CategoryQuery(
    categorySchema.Query,
    competitionSchema.Query,
    winnerSchema.Query,
    graphene.ObjectType,
):
    pass

class CategoryMutation(
    # categorySchema.Mutation,
    # competitionSchema.Mutation,
    graphene.ObjectType
):
    pass