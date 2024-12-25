from graphql_auth.mutations import ObtainJSONWebToken
#from graphql_jwt.shortcuts import get_token
import graphene

class CustomTokenAuth(ObtainJSONWebToken):

	class Arguments:
		entity = graphene.String()

	@classmethod
	def resolve(cls, root, info, **kwargs):
		result = super().resolve(root, info, **kwargs)
		
		if result.success:
			user = result.user
			

		return result



