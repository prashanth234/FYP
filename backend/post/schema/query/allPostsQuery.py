import graphene
from graphql import GraphQLError
# from django.core.paginator import Paginator
from django.utils import dateparse

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostListType import PostListType


class AllPostsQuery(graphene.ObjectType):

    all_posts = graphene.Field(
        PostListType,
        category= graphene.ID(),
        competition=graphene.ID(),
        per_page=graphene.Int(),
        cursor=graphene.String()
    )

    def resolve_all_posts(root, info, category=None, competition=None, per_page=10, cursor=None):

        if competition:
            queryset = Post.objects.filter(competition=competition).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category).order_by('-created_at')
        else:
            raise GraphQLError("Interest or Contest not found.")

        total = queryset.count()
        
        if cursor:
            queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)

    
    

    
    
        