from graphene_django import DjangoObjectType
import graphene
from entity.models import Entity
from post.models.Post import Post

class EntityType(DjangoObjectType):

  stats = graphene.JSONString()

  def resolve_stats(self, info):
    posts = Post.objects.filter()
    


  class Meta:
    model = Entity
    fields = ("id", "name", "description")