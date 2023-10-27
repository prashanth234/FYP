from graphene_django import DjangoObjectType
from core.models.User import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "avatar", "points", "gender", "first_name", "last_name", "email", "id")
    
    # def resolve_avatar(self, info):
    #     if self.avatar:
    #         self.avatar = info.context.build_absolute_uri(self.avatar.url)
    #     return self.avatar