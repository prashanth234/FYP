import graphene
from graphene_file_upload.scalars import Upload
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction

# Models
from entity.models.Verification import Verification
from entity.models.Entity import Entity

# Authentication
from graphql_jwt.decorators import login_required

import logging

logger = logging.getLogger(__name__)

class CreateEntityMutation(graphene.Mutation):

  class Arguments:
    # The input arguments for this mutation
    name = graphene.String(required=True)
    description = graphene.String()
    type = graphene.String(required=True)
    type_others = graphene.String()
    image = Upload()
    city = graphene.String(required=True)
    proof = Upload(required=True)

  # The class attributes define the response of the mutation
  success = graphene.Boolean()
  message = graphene.String()

  @classmethod
  @login_required
  @transaction.atomic
  def mutate(cls, root, info, name, type, city, proof=None, image=None, type_others=None, description=None):

    user = info.context.user

    logger.info(f'User: {user.username} - requested for creation of entity: {name}')

    entity = Entity(
      name=name,
      type=type,
      city=city,
      image=image,
      type_others=type_others,
      description=description
    )

    entity.save()

    # proof = SimpleUploadedFile("updated_file.txt", b"Updated file content")
    verification = Verification(user=user, entity=entity, request='CREATE')
    verification.file = proof
    verification.save()

    logger.info(f'User: {user.username} - entity creation request successfull. entity: {entity.id}, verifiaction: {verification.id}')

    return CreateEntityMutation(success=True, message='Entity request successfully created. Your entity will be visible once verified.')
    
class CreateEntity(graphene.ObjectType):
  create_entity = CreateEntityMutation.Field()