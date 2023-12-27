import graphene
from graphene_django import DjangoObjectType

# Models
from core.models.CoinActivity import CoinActivity


class CoinActivitiesType(DjangoObjectType):

    class Meta:
        model = CoinActivity
        fields = ("id", "status", "points", "created_at", "type", "description", "comments")