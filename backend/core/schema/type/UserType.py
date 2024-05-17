from graphene_django import DjangoObjectType
from core.models.User import User
from graphene import ObjectType, Boolean, List, String
from helpers.url_type import AvatartUrlType

class UserType(AvatartUrlType, DjangoObjectType):

    class Meta:
        model = User
        fields = ("username", "avatar", "id")
        # "points", "gender", "first_name", "last_name", "email", "phone"
    
    # def resolve_avatar(self, info):
    #     if self.avatar:
    #         self.avatar = info.context.build_absolute_uri(self.avatar.url)
    #     return self.avatar

class UserCreationCheckType(ObjectType):
    success = Boolean()
    errors = List(String)