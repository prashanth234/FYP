import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone

# Models
from categories.models.Competition import Competition

# Type
from core.schema.type.RewardsType import RewardsType


class CompetitionType(DjangoObjectType):

    expired = graphene.Boolean()

    def resolve_expired(self, info):
        current_datetime = timezone.now()
        return self.last_date <= current_datetime.date()

    class Meta:
        model = Competition
        fields = ("id", "name", "description", "category", "last_date", "image", "expired", "points")