import graphene
from graphql import GraphQLError
from django.utils import dateparse

from post.models.Post import Post
from post.schema.type.PostType import PostType
from entity.models.Entity import Entity

class EntityPostsType(graphene.ObjectType):
  posts = graphene.List(PostType)
  total = graphene.Int()

class EntityPosts(graphene.ObjectType):

  entity_posts = graphene.Field(
    EntityPostsType,
    entity=graphene.ID(required=True),
    per_page=graphene.Int(),
    cursor=graphene.String()
  )

  def resolve_entity_posts(root, info, entity, per_page=10, cursor=None):

    entity = Entity.objects.get(pk=entity)
    user = info.context.user

    if not entity.ispublic and not (user.is_authenticated and user.user_of_entities.filter(pk=user.id).exists()):
      raise GraphQLError("Failed to get posts.")

    queryset = Post.objects.filter(entity=entity).order_by('-created_at')
    total = queryset.count()
    
    if cursor:
      queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
    
    posts = queryset[:per_page]

    return EntityPostsType(posts=posts, total=total)