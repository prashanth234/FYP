from graphene_django import DjangoObjectType

from core.models.Reward import Reward

from helpers.urlType import ImageUrlType

class RewardsType(ImageUrlType, DjangoObjectType):

    class Meta:
        model = Reward
        fields = ("id", "image", "name", "points", "type", "pointsvalue")