import graphene

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostListType import PostListType


class TrendingPostsQuery(graphene.ObjectType):

    trending_posts = graphene.Field(
        PostListType,
        competition=graphene.ID(required=True)
    )

    def resolve_trending_posts(root, info, competition=None):

        top_posts = (Post.objects.filter(likes__gte=5, competition=competition, is_bot=False)
                    .select_related('category', 'user')
                    .prefetch_related('postfile_set')
                    .order_by('-likes', 'created_at')[:5])
        
        return PostListType(posts=top_posts, total=len(top_posts))

    
    

    
    
        