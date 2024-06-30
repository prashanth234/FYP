import graphene
from django.utils import dateparse
from graphql import GraphQLError

# Models
from post.models.Post import Post
from categories.models.Winner import Winner, Competition

# Type
from post.schema.type.PostListType import PostListType


class CompetitionPostsQuery(graphene.ObjectType):

  competition_posts = graphene.Field(
    PostListType,
    competition=graphene.ID(required=True),
    cp_type=graphene.String(),
    per_page=graphene.Int(),
    cursor=graphene.String()
  )

  def resolve_competition_posts(root, info, competition, cp_type='all', per_page=10, cursor=None):
    # Get competition posts

    competition = Competition.objects.select_related('entity').get(id=competition)
    user = info.context.user
    entity = competition.entity

    if not entity.ispublic and not (user.is_authenticated and info.context.user.user_of_entities.filter(pk=entity.id).exists()):
      raise GraphQLError("No Access: Failed to get posts.")
    
    if cp_type == 'allposts':

      queryset = Post.objects.filter(competition=competition, ispublic=True).order_by('-created_at')
      total = queryset.count()

      if cursor:
        queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))

      return PostListType(posts=queryset, total=total)
    
    elif cp_type == 'trending':

      top_posts = Post.objects.filter(likes__gte=5, competition=competition, is_bot=False).order_by('-likes', 'created_at')[:5]
      return PostListType(posts=top_posts, total=len(top_posts))
    
    elif cp_type == 'winners':
      
      winners = (Winner.objects.filter(competition=competition)
                .select_related('post')
                .order_by('position'))
      
      posts = []
      
      for winner in winners:
        posts.append(winner.post)

      return PostListType(posts=posts, total=len(posts))



    

    
    

    
    
        