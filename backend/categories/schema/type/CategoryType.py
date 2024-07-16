from graphene_django import DjangoObjectType
from helpers.urlType import ImageUrlType
import graphene

# Models
from categories.models.Category import Category
from categories.models.Competition import Competition

# Type
from categories.schema.type.CompetitionType import CompetitionType

class CategoryType(ImageUrlType, DjangoObjectType):

    competitions = graphene.List(CompetitionType)

    def resolve_competitions(self, info):
        return Competition.objects.filter(category_id=self.id, entity_id='1')

    class Meta:
        model = Category
        fields = ("id", "name", "description", "oftype", "key", "image", "competitions")