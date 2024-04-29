import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.core.files.base import ContentFile
from django.db import transaction
from PIL import Image
import logging

# Models
from post.models.Post import Post, PostFile

# Type
from post.schema.type.PostType import PostType

# Authentications
from graphql_jwt.decorators import login_required

# Tasks
from post.tasks import process_image


logger = logging.getLogger(__name__)

class UpdatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)
        description = graphene.String()
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id, file=None, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        try:
            post = Post.objects.get(pk=id, user=info.context.user)
            if post.competition and post.competition.is_expired:
                raise GraphQLError("You can't delete or edit posts in closed contests to ensure fairness and transparency. Thanks for understanding!", extensions={'status': 405})
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")
        
        if description != None:
            post.description = description

        post.save()

        if file and post.category.oftype != 'TEXT':
            postFile = PostFile.objects.get(post=post)

            filetype = file.content_type.split('/')[1]
            folder = f"post_{post.id}"
            filename = f"user_{info.context.user.id}/{folder}/{folder}.{filetype}"
            file_content = ContentFile(file.read())
            img = Image.open(file_content)
            width, height = img.size

            postFile.width = width
            postFile.height = height

            # Save the updated file with the new filename
            postFile.file.save(filename, file_content)

            # Process image further in background
            # process_image.delay(postFile.get_absolute_path())
            process_image(postFile.get_absolute_path())
            
            #remove_exisiting_files_in_dir(postFile.file.name)

        return UpdatePostMutation(post=post)