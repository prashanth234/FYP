import graphene
from graphene_file_upload.scalars import Upload
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from graphql import GraphQLError

# Models
from entity.models.Verification import Verification
from entity.models.Entity import Entity

# Types
from entity.schema.type.EntityType import EntityType

# Authentication
from graphql_jwt.decorators import login_required

import logging

logger = logging.getLogger(__name__)

class JoinEntityMutation(graphene.Mutation):

  class Arguments:
    # The input arguments for this mutation
    entity_id = graphene.ID(required=True)
    code = graphene.String()
    file = Upload()

  # The class attributes define the response of the mutation
  success = graphene.Boolean()
  message = graphene.String()
  entity = graphene.Field(EntityType)

  @classmethod
  @login_required
  def mutate(cls, root, info, entity_id, code=None, file=None):

    user = info.context.user

    if code == None and file == None:
      logger.error(f'User: {user.username} - trying to join the entity without file or code')
      raise GraphQLError("Category with this ID does not exist.")
    
    try:
      entity = Entity.objects.get(pk=entity_id, verified=True)
    except Entity.DoesNotExist:
      raise GraphQLError("Entity not found.")
    
    if entity.users.filter(id=user.id).exists():
      return JoinEntityMutation(success=False, message='User is already part of the entity.')
    
    success = True

    if code:
      if entity.code == code:
        entity.users.add(user)
        entity.save()
        logger.info(f'User: {user.username} - Added to the entity: {entity.id}')
        message = "Success! You've been successfully added to the entity."
      else:
        logger.error(f'User: {user.username} - Failed to add user to entity: {entity} due to wrong code: {code}.')
        message = "Invalid code! We couldn't add you to the entity. Please use the code provided by the entity."
        success = False
    else:
      # updated_file = SimpleUploadedFile("updated_file.txt", b"Updated file content")r
      verification, created = Verification.objects.get_or_create(user=user, entity=entity, request='JOIN')
      
      filetype = file.content_type.split('/')[1]
      directory = f"internal/verifications/join_entity_{entity_id}"
      filename = f"user_{user.id}.{filetype}"
      path = f"{directory}/{filename}"

      verification.file.save(path, file, save=False)
      verification.status = 'PENDING'
      verification.save()
      logger.info(f'User: {user.username} - Verification is created id: {verification.id}')
      message = "Your request is being processed. Once verified, you'll be added to the entity."

    return JoinEntityMutation(success=success, message=message, entity=entity)
    
class JoinEntity(graphene.ObjectType):
  join_entity = JoinEntityMutation.Field()