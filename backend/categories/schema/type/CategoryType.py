from graphene_django import DjangoObjectType
from helpers.url_type import ImageUrlType

# Models
from categories.models.Category import Category

class CategoryType(ImageUrlType, DjangoObjectType):

    class Meta:
        model = Category
        fields = ("id", "name", "description", "oftype", "key", "image", "competition_set")