import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Redeem import Redeem


class RedeemType(DjangoObjectType):

    class Meta:
        model = Redeem
        fields = ("id", "status", "points", "created_at")