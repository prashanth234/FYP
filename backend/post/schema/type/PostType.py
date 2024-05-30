import graphene
from graphene_django import DjangoObjectType
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from fyp.customStorage import CustomS3Storage

# Models
from post.models.Post import Post, PostFile
from post.models.Like import *

# Type
from core.schema.type.UserType import UserType

class FilesType(graphene.ObjectType):

    lg = graphene.String()
    md = graphene.String()
    og = graphene.String()

class PostFileType(DjangoObjectType):

    files = graphene.Field(FilesType)

    def resolve_files(self, info):

        if isinstance(default_storage, CustomS3Storage):

            isprivate = not self.post.ispublic
            name = self.file.name

            files = {
                "lg": default_storage.url(name.replace(".jpeg", "_lg.webp"), signed=isprivate),
                "md": default_storage.url(name.replace(".jpeg", "_md.webp"), signed=isprivate),
                "og": default_storage.url(name, signed=isprivate)
            }

        else:

            name = self.file.url

            files = {
                "lg": name.replace(".jpeg", "_lg.webp"),
                "md": name.replace(".jpeg", "_md.webp"),
                "og": name
            }

        return FilesType(**files)
    
    class Meta:
        model = PostFile
        fields = ("width", "height", "file", "files")     


class PostType(DjangoObjectType):
    
    user = graphene.Field(UserType)    
    like_count = graphene.Int()
    user_liked = graphene.Boolean()
    likes = graphene.Int()

    def resolve_like_count(self, info):
        return Like.objects.filter(item_type=ContentType.objects.get_for_model(self), item_id=self.id).count()
    
    def resolve_user_liked(self, info):
        if not info.context.user.is_authenticated:
            return False
        
        liked = Like.objects.filter(item_type=ContentType.objects.get_for_model(self), item_id=self.id, user=info.context.user)

        return True if liked else False
    
    class Meta:
        model = Post
        fields = ("id", "description", "user", "category", "competition", "postfile_set", "like_count", "user_liked", "likes", "created_at", 'is_bot', 'ispublic')
        # filter_fields = ["category", "competition"]
        # interfaces = (graphene.relay.Node, )