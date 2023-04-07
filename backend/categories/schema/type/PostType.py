import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Post import Post, PostFile
from core.models.User import User

class PostFileType(DjangoObjectType):
    class Meta:
        model = PostFile
        fields = ("file",)
    
    def resolve_file(self, info):
        if self.file:
            self.file = info.context.build_absolute_uri(self.file.url)
        return self.file

# ** See if you can decouple from this app
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username",)

class PostType(DjangoObjectType):
    # files = graphene.List(PostFileType)

    # def resolve_files(self, info):
    #     return PostFile.objects.filter(post=self)
    
    user = graphene.Field(UserType)
    
    class Meta:
        model = Post
        fields = ("id", "description", "user", "category", "competition", "postfile_set")