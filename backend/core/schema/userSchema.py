import graphene
from authentication import mutations
from authentication.queries import MeQuery

from core.schema.mutation.registerMutation import VerifyAndRegisterMutation, ChangePasswordMutation
from core.schema.mutation.verifyTokenMutation import CustomVerifyToken
from core.schema.mutation.userAvatarMutation import UserAvatarMutation
from core.schema.mutation.tokenAuthMutation import CustomTokenAuth

from core.schema.query.userAvailableQuery import UserAvailableQuery
from core.schema.query.userCreationQuery import UserCreationCheckQuery
from core.schema.query.userQuery import UserQuery

class AuthMutation(graphene.ObjectType):
  register = VerifyAndRegisterMutation.Field()
  # register = mutations.Register.Field()
  verify_account = mutations.VerifyAccount.Field()
  resend_activation_email = mutations.ResendActivationEmail.Field()
  send_password_reset_email = mutations.SendPasswordResetEmail.Field()
  password_reset = mutations.PasswordReset.Field()
  change_password = ChangePasswordMutation.Field()
  # password_change = mutations.PasswordChange.Field()
  # archive_account = mutations.ArchiveAccount.Field()
  # delete_account = mutations.DeleteAccount.Field()
  update_account = mutations.UpdateAccount.Field()
  # send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
  # verify_secondary_email = mutations.VerifySecondaryEmail.Field()
  # swap_emails = mutations.SwapEmails.Field()
  update_avatar = UserAvatarMutation.Field()
  # update_account = UpdateAccountMutation.Field()

  # django-graphql-jwt inheritances.
  token_auth = CustomTokenAuth.Field()
  verify_token = CustomVerifyToken.Field()
  refresh_token = mutations.RefreshToken.Field()
  revoke_token = mutations.RevokeToken.Field()
        
class AuthQuery(
  UserCreationCheckQuery,
  UserAvailableQuery,
  # UserQuery,
  MeQuery,
  UserQuery,
  graphene.ObjectType
):
  pass

        
        
