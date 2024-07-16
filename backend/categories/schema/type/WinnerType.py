from graphene_django import DjangoObjectType

# Models
from categories.models.Winner import Winner


class WinnerType(DjangoObjectType):

    class Meta:
        model = Winner
        convert_choices_to_enum = False
        fields = ("id", "user", "won_by_likes", "post", "competition", "position", "points")