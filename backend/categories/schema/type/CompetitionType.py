from graphene_django import DjangoObjectType

# Models
from categories.models.Competition import Competition

class CompetitionType(DjangoObjectType):
    class Meta:
        model = Competition
        fields = ("id", "name", "description", "category")