import graphene
from graphql import GraphQLError
from django.core.paginator import Paginator
from graphene_file_upload.scalars import Upload
from graphene_django.filter import DjangoFilterConnectionField

# Models
from categories.models.Competition import Competition
from categories.models.Category import Category
from categories.models.Post import Post, PostFile

# Type
from categories.schema.type.PostType import PostType


class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        description = graphene.String()
        category = graphene.ID()
        competition = graphene.ID()
        file = Upload(required=True)


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, file, description='', category=None, competition=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if not category and not competition:
            raise GraphQLError("CREATION FAILED: Post should be assoiated with either category or competition", extensions={'status': 404})

        if competition:
            competition = Competition.objects.get(pk=competition)
            category = competition.category
        elif category:
            category = Category.objects.get(pk=category)

        post = Post(
            user=info.context.user,
            description=description,
            category=category,
            competition=competition or None
        )
        
        post.save()

        postFile = PostFile(
            file=file,
            post=post
        )

        postFile.save()

        return CreatePostMutation(post=post)
    
class UpdatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)
        description = graphene.String()
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, file=None, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        try:
            post = Post.objects.get(pk=id, user=info.context.user)
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")
        
        if description:
            post.description = description

        post.save()

        if file:
            postFile = PostFile.objects.get(post=post)
            postFile.file = file
            postFile.save()

        return UpdatePostMutation(post=post)

class DeletePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)


    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        try:
            post = Post.objects.get(pk=id, user=info.context.user)
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")
        
        post.delete()

        return DeletePostMutation(success=True)
    
class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()

class PostListType(graphene.ObjectType):
    posts = graphene.List(PostType)
    total = graphene.Int()

class Query(graphene.ObjectType):

    # post = graphene.relay.Node.Field(PostType)
    # all_posts = DjangoFilterConnectionField(PostType)

    all_posts = graphene.Field(PostListType, category= graphene.Int(), competition=graphene.Int(), page=graphene.Int(), per_page=graphene.Int(), trending=graphene.Boolean())

    def resolve_all_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False):

        # If trending flag is set return top number of posts
        if trending:
            top_posts = Post.objects.filter(competition=competition).order_by('-likes')[:per_page]
            return PostListType(posts=top_posts, total=len(top_posts))

        if competition:
            queryset = Post.objects.filter(competition=competition).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category).order_by('-created_at')
        else:
            queryset = Post.objects.all().order_by('-created_at')

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.page(page)
        posts = page_obj.object_list

        # Return paginated list of posts
        return PostListType(posts=posts, total=page_obj.paginator.count)
    
    my_posts = graphene.Field(PostListType, category= graphene.Int(), competition=graphene.Int(), page=graphene.Int(), per_page=graphene.Int(), trending=graphene.Boolean())
    
    def resolve_my_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if competition:
            queryset = Post.objects.filter(competition=competition, user=info.context.user).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category, user=info.context.user).order_by('-created_at')
        else:
            queryset = Post.objects.filter(user=info.context.user).order_by('-created_at')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.page(page)
        posts = page_obj.object_list

        # Return paginated list of posts
        return PostListType(posts=posts, total=page_obj.paginator.count)
    
    post_details = graphene.Field(PostType, id=graphene.Int())

    def resolve_post_details(root, info, id):
        return Post.objects.get(pk=id)
        