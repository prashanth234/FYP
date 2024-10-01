import graphene
from django.core.files.storage import default_storage
from fyp.customStorage import CustomS3Storage

# Models
from entity.models.Verification import Verification

from core.schema.type.UserType import UserType


class JoinRequestType(graphene.ObjectType):

  files = graphene.List(graphene.String)
  id = graphene.String()
  user = graphene.Field(UserType)

  def resolve_files(self, info):

    if isinstance(default_storage, CustomS3Storage):
      return [default_storage.url(self.file.name, signed=True)]
    else:
      return [self.file.url]

  def resolve_id(self, info):
    return self.id

  class Meta:
    model = Verification
    fields = (
      "id"
    )
  
