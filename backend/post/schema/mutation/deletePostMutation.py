import graphene
from graphql import GraphQLError
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
import logging

# Models
from post.models.Post import Post, PostFile
from core.models.CoinActivity import CoinActivity
from entity.schema.type.EntityType import EntityType

# Authentications
from graphql_jwt.decorators import login_required


logger = logging.getLogger(__name__)

class DeletePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)


    # The class attributes define the response of the mutation
    success = graphene.Boolean()
    ca_id = graphene.ID()
    entity = graphene.Field(EntityType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id):

        ca_id = None
        
        try:
            user = info.context.user
            logger.info(f"User: {user.username} - intiatied the post deletion.")
            post = Post.objects.select_related("entity").get(pk=id)
            entity = post.entity

            if post.competition and post.competition.is_expired:
                raise GraphQLError("You can't delete or edit posts in closed contests to ensure fairness and transparency. Thanks for understanding! ")
            
            # Either user who owns can delete or entity admin in which it is posted can delete the post.
            if post.user != user and not user.admin_of_entities.filter(pk=entity.id).exists():
                logger.warning(f"User: {user.username} - post: {id} - Unauthorized Action for post deletion")
                raise GraphQLError("Unauthorized Action.")
            
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")

        if post.competition:
            try:
                content_type = ContentType.objects.get_for_model(Post)
                coinactivity = CoinActivity.objects.get(object_id=id, content_type=content_type)
                ca_id = coinactivity.id
                coinactivity.delete()
            except CoinActivity.DoesNotExist:
                pass

        post.delete()
        logger.info(f"User: {user.username} - post: {id} - post deletion completed.")

        return DeletePostMutation(success=True, ca_id=ca_id, entity=entity)
    
class DeletePost(graphene.ObjectType):
    delete_post = DeletePostMutation.Field()
    

    
    
        