import graphene
from post.schema.type.PostType import PostType

class PostListType(graphene.ObjectType):
    posts = graphene.List(PostType)
    total = graphene.Int()