import graphene
from graphql import GraphQLError
from django.utils import dateparse

from post.models.Post import Post
from post.schema.type.PostType import PostType
from entity.models.Entity import Entity
from categories.models.Competition import Competition

class EntityPostsType(graphene.ObjectType):
  posts = graphene.List(PostType)
  total = graphene.Int()

class EntityPosts(graphene.ObjectType):

  entity_posts = graphene.Field(
    EntityPostsType,
    entity=graphene.ID(required=True),
    competition=graphene.ID(),
    per_page=graphene.Int(),
    cursor=graphene.String()
  )

  def resolve_entity_posts(root, info, entity, competition=None, per_page=10, cursor=None):

    entity = Entity.objects.get(pk=entity)
    user = info.context.user

    if not entity.ispublic and not (user.is_authenticated, user.user_of_entities.filter(pk=entity.id).exists()):
      raise GraphQLError("Failed to get posts.")
    
    if competition:
      queryset = Post.objects.filter(competition_id=competition, entity=entity).order_by('-created_at')
    else:
      queryset = Post.objects.filter(entity=entity).order_by('-created_at')

    total = queryset.count()
    
    if cursor:
      queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
    
    posts = queryset[:per_page]

    return EntityPostsType(posts=posts, total=total)