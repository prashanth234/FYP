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
        
        user = info.context.user
        
        try:
            post = Post.objects.get(pk=id, user=user)
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
            post_folder = f"post_{post.id}"
            root_dir = 'public' if post.ispublic else 'private'
            directory = f"{root_dir}/posts/user_{user.id}/{post_folder}"
            filename = f"{post_folder}.{filetype}"
            path = f"{directory}/{filename}"

            file_content = ContentFile(file.read())
            img = Image.open(file_content)
            width, height = img.size

            postFile.width = width
            postFile.height = height

            postFile._context = {'file': postFile.file.name}
            # Save the updated file with the new filename
            postFile.file.save(path, file_content)

            # Process image further in background
            # process_image.delay(postFile.get_absolute_path())
            process_image(img, postFile.file.name)

        return UpdatePostMutation(post=post)
    
class UpdatePost(graphene.ObjectType):
    update_post = UpdatePostMutation.Field()