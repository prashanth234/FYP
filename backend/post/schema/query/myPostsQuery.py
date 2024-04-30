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
        page=graphene.Int(),
        per_page=graphene.Int(),
        trending=graphene.Boolean(),
        cursor=graphene.String()
    )
    
    def resolve_my_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False, cursor=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if competition:
            queryset = Post.objects.filter(competition=competition, user=info.context.user).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category, user=info.context.user).order_by('-created_at')
        else:
            queryset = Post.objects.filter(user=info.context.user).order_by('-created_at')
        
        # paginator = Paginator(queryset, per_page)
        # page_obj = paginator.page(page)
        # posts = page_obj.object_list

        total = queryset.count()
        
        if cursor:
           queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)

    
    

    
    
        