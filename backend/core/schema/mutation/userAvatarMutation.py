import graphene
from graphene_file_upload.scalars import Upload
from django.core.files.base import ContentFile
from datetime import datetime
from graphql import GraphQLError

# Authentications
from graphql_jwt.decorators import login_required

# Type
from core.schema.type.UserType import UserType

class UserAvatarMutation(graphene.Mutation):

	class Arguments:
		avatar = Upload()
		type = graphene.String()

	user = graphene.Field(UserType)

	@classmethod
	@login_required
	def mutate(cls, root, info, avatar, type):

		if not avatar:
			raise GraphQLError("Avatar not found", extensions={'status': 404})
		
		user = info.context.user
		
		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		filename = f"{user.username}_{timestamp}.{type}"
		file_content = ContentFile(avatar.read())

		# Remove the existing file if it exists
		if user.avatar:
			user.avatar.storage.delete(user.avatar.name)

		# Save the updated file with the new filename
		user.avatar.save(filename, file_content)

		# Save the MyModel instance to update other fields if needed
		# user.avatar.save(filename, file_content, save=False)
		# user.save()

		# Remove the existing file if it exists
		# if original_filename:
		#     file_path = os.path.join(settings.MEDIA_ROOT, original_filename)
		#     if os.path.exists(file_path):
		#         os.remove(file_path)

		return UserAvatarMutation(user=user)