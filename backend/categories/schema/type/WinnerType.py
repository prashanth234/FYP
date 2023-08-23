import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Winner import Winner


class WinnerType(DjangoObjectType):

    class Meta:
        model = Winner
        fields = ("id", "user", "likes", "post", "competition")