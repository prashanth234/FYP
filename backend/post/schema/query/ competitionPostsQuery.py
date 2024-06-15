import graphene
from django.utils import dateparse

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostListType import PostListType


class CompetitionPostsQuery(graphene.ObjectType):

  competition_posts = graphene.Field(
    PostListType,
    competition=graphene.ID(required=True),
    type=graphene.String()
  )

  def resolve_competition_posts(root, info, competition, type='all', per_page=10, cursor=None):
    # Get competition posts
    if type == 'all':

      queryset = Post.objects.filter(competition=competition, ispublic=True).order_by('-created_at')
      total = queryset.count()
      queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
      return PostListType(posts=queryset, total=total)
    
    elif type == 'trending':

      top_posts = Post.objects.filter(likes__gte=5, competition=competition, is_bot=False).order_by('-likes', 'created_at')[:5]
      return PostListType(posts=top_posts, total=len(top_posts))
    
    elif type == 'winners':
      pass


    

    
    

    
    
        