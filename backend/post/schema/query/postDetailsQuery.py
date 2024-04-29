import graphene

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostType import PostType
 
class PostDetailsQuery(graphene.ObjectType):
    post_details = graphene.Field(
        PostType,
        id=graphene.ID(required=True),
        category=graphene.ID()
    )

    def resolve_post_details(root, info, id, category):
        return Post.objects.get(pk=id, category__id=category)


    
    

    
    
        