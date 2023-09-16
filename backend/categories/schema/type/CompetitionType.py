import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone

# Models
from categories.models.Competition import Competition
from categories.models.Post import Post

# Types
from categories.schema.type.PostType import PostType


class CompetitionType(DjangoObjectType):
    # posts = graphene.List(PostType)

    # def resolve_posts(self, info):
    #     return Post.objects.filter(competition=self)

    expired = graphene.Boolean()

    def resolve_expired(self, info):
        current_datetime = timezone.now()
        return self.last_date <= current_datetime.date()

    class Meta:
        model = Competition
        fields = ("id", "name", "description", "category", "points", "last_date", "image", "expired")