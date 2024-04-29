from graphene_django import DjangoObjectType

# Models
from categories.models.Category import Category

class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = ("id", "name", "description", "oftype", "key", "image", "competition_set")