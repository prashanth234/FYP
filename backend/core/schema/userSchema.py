import graphene
import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from django.core.files.base import ContentFile

# Type
from core.schema.type.UserType import UserType

# Authentications
from graphql_jwt.decorators import login_required

class AuthQuery(
    # UserQuery,
    MeQuery,
    graphene.ObjectType
):
    pass

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
        
        filename = f"{user.username}.{type}"
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

class UpdateAccountMutation(graphene.Mutation):

    class Arguments:
        gender = graphene.String()
        firstName = graphene.String()
        lastName = graphene.String()
        dateOfBirth = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, gender=None, firstName=None, lastName=None, dateOfBirth=None, email=None):
        
        user = info.context.user
        
        if user.status.verified and email:
            raise GraphQLError("Email can't be updated, please reachout to support", extensions={'status': 403})
        
        if gender:
            user.gender = gender

        if firstName:
            user.first_name = firstName

        if lastName:
            user.last_name = lastName

        if dateOfBirth:
            user.date_of_birth = dateOfBirth
        
        if email:
            user.email = email

        user.save()

        return UpdateAccountMutation(user=user, success=True)

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    # password_change = mutations.PasswordChange.Field()
    # archive_account = mutations.ArchiveAccount.Field()
    # delete_account = mutations.DeleteAccount.Field()
    # update_account = mutations.UpdateAccount.Field()
    # send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    # verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    # swap_emails = mutations.SwapEmails.Field()
    update_avatar = UserAvatarMutation.Field()
    update_account = UpdateAccountMutation.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()