import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Category import Category
from categories.models.Competition import Competition

# Type
from categories.schema.type.CompetitionType import CompetitionType

class CategoryType(DjangoObjectType):

    competitions = graphene.List(CompetitionType)

    def resolve_competitions(self, info):
        return Competition.objects.filter(category=self)

    class Meta:
        model = Category
        fields = ("id", "name", "description", "competitions")