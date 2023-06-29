import graphene
import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.core.files.base import ContentFile


from core.models.User import User

class AuthQuery(
    # UserQuery,
    MeQuery,
    graphene.ObjectType
):
    pass

class UserType1(DjangoObjectType):
    class Meta:
        model = User
        fields = ("avatar",  "username")

    def resolve_avatar(self, info):
        if self.avatar:
            self.avatar = info.context.build_absolute_uri(self.avatar.url)
        return self.avatar

class UserAvatarMutation(graphene.Mutation):

    class Arguments:
        avatar = Upload()
        type = graphene.String()

    user = graphene.Field(UserType1)

    @classmethod
    def mutate(cls, root, info, avatar, type):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if not avatar:
            raise GraphQLError("Avatar not found", extensions={'status': 404})
        
        user = info.context.user
        
        filename = f"{user.username}.{type}"
        file_content = ContentFile(avatar.read())

        # Remove the existing file if it exists
        if user.avatar:
            user.avatar.storage.delete(user.avatar.name)

        # Save the updated file with the new filename
        user.avatar.save(filename, file_content, save=False)

        # Save the MyModel instance to update other fields if needed
        user.save()

        return UserAvatarMutation(user=user)

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
    update_avatar = UserAvatarMutation.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()