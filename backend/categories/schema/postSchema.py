import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

# Models
from categories.models.Competition import Competition
from categories.models.Post import Post, PostFile

# Type
from categories.schema.type.PostType import PostType


class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        description = graphene.String()
        competition = graphene.ID(required=True)
        file = Upload(required=True)


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, competition, file, description=''):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
                
        competition = Competition.objects.get(pk=competition)

        post = Post(
            user=info.context.user,
            description=description,
            category=competition.category,
            competition=competition
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
    

class Query(graphene.ObjectType):

    all_posts = graphene.List(PostType)

    def resolve_all_posts(root, info):
        return Post.objects.all()
    
    my_posts = graphene.List(PostType)
    
    def resolve_my_posts(root, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        return Post.objects.filter(user=info.context.user)
    
    post_details = graphene.Field(PostType, id=graphene.Int())

    def resolve_post_details(root, info, id):
        return Post.objects.get(pk=id)
        