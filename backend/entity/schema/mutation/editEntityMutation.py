import graphene
from graphene_file_upload.scalars import Upload
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from graphql import GraphQLError

# Models
from entity.models.Verification import Verification
from entity.models.Entity import Entity

# Authentication
from graphql_jwt.decorators import login_required

# Types
from entity.schema.type.EntityType import EntityType

import logging

logger = logging.getLogger(__name__)

class EditEntityMutation(graphene.Mutation):

  class Arguments:
    # The input arguments for this mutation
    id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()
    maps = graphene.String()
    instagram = graphene.String()
    linkedin = graphene.String()
    facebook = graphene.String()
    image = Upload()
    phone = graphene.String()
    email = graphene.String()
    city = graphene.String()

  # The class attributes define the response of the mutation
  success = graphene.Boolean()
  details = graphene.Field(EntityType)
  message = graphene.String()

  @classmethod
  @login_required
  @transaction.atomic
  def mutate(cls, root, info, 
              id,
              name=None,
              city=None,
              phone=None,
              email=None,
              instagram=None,
              linkedin=None,
              facebook=None,
              maps=None,
              image=None,
              description=None
            ):

    user = info.context.user

    logger.info(f'User: {user.username} is changing the entity details: {name}')

    if not user.admin_of_entities.filter(pk=id).exists():
      return GraphQLError("Permission Denied")
    
    try:
      entity = Entity.objects.get(pk=id)
    except Entity.DoesNotExist:
      return GraphQLError("Entity Not Found")

    if name:
      entity.name = name

    if description:
      entity.description = description

    if city:
      entity.city = city

    if instagram:
      entity.instagram = instagram

    if facebook:
      entity.facebook = facebook

    if maps:
      entity.maps = maps

    if linkedin:
      entity.linkedin = linkedin
    
    if image:
      entity.image = image

    if phone:
      entity.phone = phone

    if email:
      entity.email = email

    entity.save()

    logger.info(f'User: {user.username} - entity update successfull. entity: {entity.id}')

    return EditEntityMutation(success=True, details=entity, message='Entity updated successfully.')
    
class EditEntity(graphene.ObjectType):
  edit_entity = EditEntityMutation.Field()