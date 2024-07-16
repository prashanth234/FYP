import graphene
from graphql import GraphQLError
# from django.core.paginator import Paginator
from django.utils import dateparse

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostListType import PostListType

class MyPostsQuery(graphene.ObjectType):

    my_posts = graphene.Field(
        PostListType,
        category= graphene.ID(),
        competition=graphene.ID(),
        per_page=graphene.Int(),
        cursor=graphene.String()
    )
    
    def resolve_my_posts(root, info, category=None, competition=None, per_page=10, cursor=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if competition:
            queryset = (Post.objects.filter(competition=competition, user=info.context.user)
                        .select_related('category', 'user')
                        .prefetch_related('postfile_set')
                        .order_by('-created_at'))
        elif category:
            queryset = (Post.objects.filter(category=category, user=info.context.user)
                        .select_related('category', 'user')
                        .prefetch_related('postfile_set')
                        .order_by('-created_at'))
        else:
            queryset = (Post.objects.filter(user=info.context.user)
                        .select_related('category', 'user')
                        .prefetch_related('postfile_set')
                        .order_by('-created_at'))


        total = queryset.count()
        
        if cursor:
           queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)

    
    

    
    
        