import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone

# Models
from categories.models.Competition import Competition

# Type
from categories.schema.type.RewardsType import RewardsType


class CompetitionType(DjangoObjectType):

    expired = graphene.Boolean()

    def resolve_expired(self, info):
        current_datetime = timezone.now()
        return self.last_date <= current_datetime.date()
    
    rewards = graphene.List(RewardsType)

    def resolve_rewards(self, info):
        return self.rewards.all()

    class Meta:
        model = Competition
        fields = ("id", "name", "description", "category", "last_date", "image", "expired")