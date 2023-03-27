from graphene_django import DjangoObjectType

# Models
from categories.models.Competation import Competation

class CompetationType(DjangoObjectType):
    class Meta:
        model = Competation
        fields = ("id", "name", "description", "category")