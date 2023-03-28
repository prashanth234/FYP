import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Competition import Competition
from categories.models.Post import Post

# Types
from categories.schema.type.PostType import PostType

class CompetitionType(DjangoObjectType):
    posts = graphene.List(PostType)

    def resolve_posts(self, info):
        return Post.objects.filter(competition=self)

    class Meta:
        model = Competition
        fields = ("id", "name", "description", "category", "posts")