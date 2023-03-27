import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

# Models
from categories.models.Competation import Competation
from categories.models.Category import Category
from categories.models.Post import Post, PostImage
# **Make this model losely coupled
from core.models.User import User


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "description", "user", "category", "competation")

class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        user = graphene.ID(required=True)
        description = graphene.String()
        category = graphene.ID(required=True)
        competation = graphene.ID(required=True)
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, user, category, competation, file, description=''):
        user = User.objects.get(pk=user)
        category = Category.objects.get(pk=category)
        competation = Competation.objects.get(pk=competation)

        post = Post(
            user=user,
            description=description,
            category=category,
            competation=competation
        )

        post.save()

        postImage = PostImage(
            image=file,
            post=post
        )

        postImage.save()

        return CreatePostMutation(post=post)

class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    

class Query(graphene.ObjectType):

    all_Posts = graphene.List(PostType)

    def resolve_all_post(root, info):
        return Post.objects.all()