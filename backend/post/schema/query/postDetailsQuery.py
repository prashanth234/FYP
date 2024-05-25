import graphene
from graphql import GraphQLError

# Models
from post.models.Post import Post

# Type
from post.schema.type.PostType import PostType

import logging

logger = logging.getLogger(__name__)
 
class PostDetailsQuery(graphene.ObjectType):
    post_details = graphene.Field(
        PostType,
        id=graphene.ID(required=True),
        category=graphene.ID(),
        entity=graphene.ID()
    )

    def resolve_post_details(root, info, id, category=None, entity=None):
        user = info.context.user

        try:
            if category:
                post = Post.objects.get(pk=id, category__id=category)
            elif entity:
                post = Post.objects.get(pk=id, entity__id=entity)
        except Post.DoesNotExist:
            raise GraphQLError('NOTFOUND')

        logger.info(f'User: {user.username} - requested for post {post.id}')

        if not post.ispublic or not (user.is_authenticated or post.entity.users.filter(id=user.id).exists()):
            raise GraphQLError('Access Denied: This entity is private. Only members have access to posts.')

        return post


    
    

    
    
        