from graphene_django import DjangoObjectType

from core.models.Reward import Reward

class RewardsType(DjangoObjectType):

    class Meta:
        model = Reward
        fields = ("id", "image", "name", "points", "position", "type", "realvalue")