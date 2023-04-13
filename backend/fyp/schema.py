import graphene

# ** Move user realted schema and mutations to user app
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from categories.schema import CategoryQuery, CategoryMutation

# from core.models.User import User

# class CustomRegistrationMutation(mutations.Register):
#     firstname = graphene.String(required=True)
    
#     def mutate(self, info, password, **kwargs):
#         # get your custom fields from kwargs
#         user = User(**kwargs)
#         user.set_password(password)
#         user.save()
#         # set your custom fields to the user instance
#         return CustomRegistrationMutation(user=user)

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

class Query(CategoryQuery, UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, CategoryMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)