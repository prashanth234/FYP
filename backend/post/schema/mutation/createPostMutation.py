import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import transaction
from PIL import Image
import logging

# Models
from categories.models.Competition import Competition
from categories.models.Category import Category
from post.models.Post import Post, PostFile
from core.models.CoinActivity import CoinActivity
from entity.models.Entity import Entity
from entity.models.Verification import Verification

# Type
from post.schema.type.PostType import PostType
from entity.schema.type.EntityType import EntityType
from core.schema.type.CoinActivityType import CoinActivitiesType

# Authentications
from graphql_jwt.decorators import login_required

# Tasks
from post.tasks import process_image

logger = logging.getLogger(__name__)

class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        description = graphene.String()
        category = graphene.ID()
        competition = graphene.ID()
        file = Upload()
        entity = graphene.ID(required=True)


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)
    coin_activity = graphene.Field(CoinActivitiesType)
    entity = graphene.Field(EntityType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, entity, file=None, description='', category=None, competition=None):

        user = info.context.user
        logger.info(f"User: {user.username} - intiatied the post creation.")
        
        if not category and not competition:
            raise GraphQLError("Almost there! To continue, kindly pick your interest.", extensions={'status': 404})

        if competition:
            competition = Competition.objects.get(pk=competition)

            if competition.is_expired:
                raise GraphQLError("The contest has concluded! Please take a look at our other ongoing contests.", extensions={'status': 405})
            
            if Post.objects.filter(competition=competition, user=info.context.user).exists():
                raise GraphQLError("To maintain fairness, kindly note that each user is permitted only one post per contest.", extensions={'status': 405})
            
            category = competition.category
        elif category:
            category = Category.objects.get(pk=category)

        # Check if user part of entity if not check if verification is pending
        entity = Entity.objects.get(pk=entity, verified=True)

        if not user.user_of_entities.filter(pk=entity.id).exists():
            try:
                Verification.objects.get(user=user, entity=entity, status='PENDING')
            except Verification.DoesNotExist:
                raise GraphQLError("Failed: Join the entity first to post within it.", extensions={'status': 403})

        post = Post(
            user=user,
            description=description,
            category=category,
            competition=competition or None,
            entity=entity,
            ispublic=entity.ispublic
        )
        
        post.save()

        coinactivity = None

        if competition:
            ca_description = f'{competition.name} Contest - Participation Reward'
            coinactivity = CoinActivity(
                type='COMPPARTN',
                user=user,
                points=settings.COMPPARTN_POINTS,
                description=ca_description,
                content_object=post,
                status='Q'
            )
            coinactivity.save()

        if file:

            filetype = file.content_type.split('/')[1]

            post_folder = f"post_{post.id}"
            root_dir = 'public' if post.ispublic else 'private'
            directory = f"{root_dir}/posts/user_{user.id}/{post_folder}"
            filename = f"{post_folder}.{filetype}"
            path = f"{directory}/{filename}"

            logger.info(f"{path} processing started.")

            file_content = ContentFile(file.read())
            img = Image.open(file_content)
            width, height = img.size

            postFile = PostFile(
                post=post,
                width=width,
                height=height
            )

            # Save the updated file with the new filename
            postFile.file.save(path, file_content, save=False)

            postFile.save()
            
            # Process image further in background
            # process_image.delay(postFile.get_absolute_path())
            process_image(img, postFile.file.name)

        logger.info(f"User: {user.username} - Post creation is successful.")
        return CreatePostMutation(post=post, coin_activity=coinactivity, entity=entity)
  
class CreatePost(graphene.ObjectType):
    create_post = CreatePostMutation.Field()

    
    
        