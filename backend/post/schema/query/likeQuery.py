import graphene
from graphql import GraphQLError

# Models
from post.models.Like import Like

class LikeCountQuery(graphene.ObjectType):

    like_count = graphene.Int(id=graphene.Int())

    def resolve_like_count(root, info, id):
        try:
            return Like.objects.filter(item_id=id).count()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise GraphQLError("Query Failed")