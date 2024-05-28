from graphene import ObjectType, String

class ImageUrlType(ObjectType):

  image = String()

  def resolve_image(self, info):
    return self.image and self.image.url
  
class AvatartUrlType(ObjectType):

  avatar = String()

  def resolve_avatar(self, info):
    return self.avatar and self.avatar.url