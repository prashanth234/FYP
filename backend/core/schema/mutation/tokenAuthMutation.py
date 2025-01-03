from authentication.mutations import ObtainJSONWebToken
import graphene
from .common import verify_entity, verify_user, verify_entity_access

class CustomTokenAuth(ObtainJSONWebToken):

	class Arguments:
		entity = graphene.String()

	@classmethod
	def mutate(cls, root, info, entity='sd', **kwargs):
		# Check if the entity exists
		if entity:
			entity_res = verify_entity(entity)
			if not entity_res["success"]:
				return cls(**entity_res)

		# Verify the login
		result = super().mutate(root, info, **kwargs)
		
		# If login is successfull, check if the user belongs the requested entity
		if result.success and entity:

			user_res = verify_user(result.payload["username"])
			response = verify_entity_access(user=user_res["user"], entity=entity_res["entity"])

			# Throw error if user doesn't belong to entity even if login is successfull
			if not response["success"]:
				return cls(**response)

		return result



