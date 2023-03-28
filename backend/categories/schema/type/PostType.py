import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Post import Post, PostFile

class PostFileType(DjangoObjectType):
    class Meta:
        model = PostFile
        fields = ("file",)

class PostType(DjangoObjectType):
    files = graphene.List(PostFileType)

    def resolve_files(self, info):
        return PostFile.objects.filter(post=self)
    
    class Meta:
        model = Post
        fields = ("id", "description", "user", "category", "competition", "files")