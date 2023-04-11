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
        try:
            post = Post.objects.get(pk=id)
            user = User.objects.get(pk=1)
            like = Like(item=post, user=user)
            like.save()
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
        try:
            Like.objects.get(pk=id).delete()
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