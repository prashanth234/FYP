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

# Type
from post.schema.type.PostType import PostType
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


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)
    coin_activity = graphene.Field(CoinActivitiesType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, file=None, description='', category=None, competition=None):

        user = info.context.user
        logger.info(f"{user.username} intiatied the post creation.")
        
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

        post = Post(
            user=user,
            description=description,
            category=category,
            competition=competition or None
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
            folder = f"post_{post.id}"
            filename = f"user_{info.context.user.id}/{folder}/{folder}.{filetype}"
            logger.info(f"{filename} processing started.")
            file_content = ContentFile(file.read())
            img = Image.open(file_content)
            width, height = img.size

            postFile = PostFile(
                post=post,
                width=width,
                height=height
            )

            # Save the updated file with the new filename
            postFile.file.save(filename, file_content, save=False)

            postFile.save()
            
            # Process image further in background
            # process_image.delay(postFile.get_absolute_path())
            process_image(postFile.get_absolute_path())

        logger.info(f"Post creation intiatied by {user.username} is successful.")
        return CreatePostMutation(post=post, coin_activity=coinactivity)

    
    

    
    
        