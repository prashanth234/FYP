import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

# Models
from categories.models.Competition import Competition
from categories.models.Category import Category
from categories.models.Post import Post, PostFile
# **Make this model losely coupled
from core.models.User import User

# Type
from categories.schema.type.PostType import PostType


class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        user = graphene.ID(required=True)
        description = graphene.String()
        category = graphene.ID(required=True)
        competition = graphene.ID(required=True)
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, user, category, competition, file, description=''):
        user = User.objects.get(pk=user)
        category = Category.objects.get(pk=category)
        competition = Competition.objects.get(pk=competition)

        post = Post(
            user=user,
            description=description,
            category=category,
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
        category = graphene.ID()
        competition = graphene.ID()
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, category=None, competition=None, file=None, description=None):
        post = Post.objects.get(pk=id)

        if not post:
            raise GraphQLError("Post with this ID does not exist.")

        if category:
            post.category = Category.objects.get(pk=category)
        
        if competition:
            post.competition = Competition.objects.get(pk=competition)
        
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
        Post.objects.get(pk=id).delete()
        return DeletePostMutation(success=True)
    

class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()
    

class Query(graphene.ObjectType):

    all_Posts = graphene.List(PostType)

    def resolve_all_post(root, info):
        return Post.objects.all()
    
    post_details = graphene.Field(PostType, id=graphene.Int())

    def resolve_post_details(root, info, id):
        return Post.objects.get(pk=id)
        