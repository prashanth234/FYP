import graphene
from graphql import GraphQLError

# Models
from categories.models.Like import Like
from categories.models.Post import Post
# **Make this model losely coupled
from core.models.User import User

class AddLikeMutation(graphene.Mutation):

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
            post = Post.objects.get(pk=id)
            post.likes += 1
            like = Like(item=post, user=info.context.user)
            like.save()
            post.save()
            return AddLikeMutation(success=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise GraphQLError("Mutation Failed")


class UnLikeMutation(graphene.Mutation):
    
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
            like = Like.objects.filter(item_id=id, user=info.context.user)
            post = Post.objects.get(pk=id)
            post.likes -= 1

            if not like:
                raise GraphQLError("User has not liked the post")
            
            like.delete()
            post.save()
            return UnLikeMutation(success=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise GraphQLError("Mutation Failed")

class Mutation(graphene.ObjectType):
    like_item = AddLikeMutation.Field()
    unlike_item = UnLikeMutation.Field()

class Query(graphene.ObjectType):

    like_count = graphene.Int(id=graphene.Int())

    def resolve_like_count(root, info, id):
        try:
            return Like.objects.filter(item_id=id).count()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise GraphQLError("Query Failed")