import graphene

from categories.schema import categorySchema, competitionSchema

class CategoryQuery(
    categorySchema.Query,
    competitionSchema.Query,
    graphene.ObjectType,
):
    pass

class CategoryMutation(
    # categorySchema.Mutation,
    # competitionSchema.Mutation,
    graphene.ObjectType
):
    pass