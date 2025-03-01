import graphene

# Models
from categories.models.Winner import Winner

# Type
from categories.schema.type.WinnerType import WinnerType

class Query(graphene.ObjectType):

    winners = graphene.List(
        WinnerType,
        competition=graphene.ID(required=True)
    )

    def resolve_winners(root, info, competition):
        return (Winner.objects.filter(competition=competition)
                .select_related('post')
                .order_by('position'))