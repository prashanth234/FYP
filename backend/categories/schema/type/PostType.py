import graphene
from graphene_django import DjangoObjectType
from django.contrib.contenttypes.models import ContentType

# Models
from categories.models.Post import Post, PostFile
from categories.models.Like import *

# Type
from core.schema.type.UserType import UserType

class PostFileType(DjangoObjectType):
    class Meta:
        model = PostFile
        fields = ("file",)
    
    # def resolve_file(self, info):
    #     if self.file:
    #         self.file = info.context.build_absolute_uri(self.file.url)
    #     return self.file


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
        fields = ("id", "description", "user", "category", "competition", "postfile_set", "like_count", "user_liked", "likes", "created_at")
        # filter_fields = ["category", "competition"]
        # interfaces = (graphene.relay.Node, )