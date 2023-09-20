from graphene_django import DjangoObjectType

from categories.models.Reward import Reward

class RewardsType(DjangoObjectType):

    class Meta:
        model = Reward
        fields = ("id", "points", "position", "type")