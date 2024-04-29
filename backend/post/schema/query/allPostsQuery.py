import graphene
from graphql import GraphQLError
# from django.core.paginator import Paginator
# from graphene_django.filter import DjangoFilterConnectionField
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
        page=graphene.Int(),
        per_page=graphene.Int(),
        trending=graphene.Boolean(),
        cursor=graphene.String()
    )

    def resolve_all_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False, cursor=None):

        # If trending flag is set return top number of posts
        # if trending:
        #     top_posts = Post.objects.filter(likes__gte=5, competition=competition).order_by('-likes', 'created_at')[:5]
        #     return PostListType(posts=top_posts, total=len(top_posts))

        if competition:
            queryset = Post.objects.filter(competition=competition).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category).order_by('-created_at')
        else:
            raise GraphQLError("Interest or Contest not found.")
            # queryset = Post.objects.all().order_by('-pk')

        # paginator = Paginator(queryset, per_page)
        # page_obj = paginator.page(page)
        # posts = page_obj.object_list

        total = queryset.count()
        
        if cursor:
            queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)

    
    

    
    
        