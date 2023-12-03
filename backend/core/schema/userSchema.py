import graphene
# import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import MeQuery
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from django.core.files.base import ContentFile
from datetime import datetime
# from graphql_auth.models import UserStatus
from core.models.User import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from core.schema.type.UserType import UserCreationCheckType
# from django.contrib.auth import get_user_model

from graphql_auth.utils import revoke_user_refresh_token
from graphql_auth.signals import user_verified

# Type
from core.schema.type.UserType import UserType

# Authentications
from graphql_jwt.decorators import login_required

# Firebase
from firebase_admin import auth

import logging

logger = logging.getLogger(__name__)

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

# class UpdateAccountMutation(graphene.Mutation):

#     class Arguments:
#         gender = graphene.String()
#         firstName = graphene.String()
#         lastName = graphene.String()
#         dateOfBirth = graphene.String()
#         email = graphene.String()
#         phone = graphene.String()

#     user = graphene.Field(UserType)
#     success = graphene.Boolean()

#     @classmethod
#     @login_required
#     def mutate(cls, root, info, gender=None, firstName=None, lastName=None, dateOfBirth=None, email=None, phone=None):
        
#         user = info.context.user
        
#         if user.status.verified and email:
#             raise GraphQLError("Email can't be updated, please reachout to support", extensions={'status': 403})
        
#         if email == "" and phone == "":
#             raise GraphQLError("Please provide either email or phone number", extensions={'status': 400})
        
#         if gender is not None:
#             user.gender = gender

#         if firstName is not None:
#             user.first_name = firstName

#         if lastName is not None:
#             user.last_name = lastName

#         if dateOfBirth:
#             user.date_of_birth = dateOfBirth
        
#         if email is not None:
#             UserStatus.clean_email(email)
#             user.email = email

#         if phone is not None:
#             if User.objects.filter(phone=phone).exists():
#                 raise GraphQLError("Phone number must be unique", extensions={'status': 400})
#             user.phone = phone

#         user.save()
        
#         return UpdateAccountMutation(user=user, success=True)

class VerifyToken:

    phone_exists = "User with this phone number already exits."

    def __init__(self, verify_type) -> None:
        
        self.verify_type = verify_type

        if verify_type == "REGISTER":
            self.failure_msg = "Failed to register user."
        elif verify_type == "CHANGEPSW":
            self.failure_msg = "Failed to change password."

    def raiseFailure(self, log_message, message=None):
        logger.error(f"{self.verify_type} - {log_message}")
        raise GraphQLError(message or self.failure_msg)

    def verify(self, token, phone=None):
        if token is None:
            self.raiseFailure("Token not found.")

        try:
            # Verify the Firebase token using the Firebase SDK
            decoded_token = auth.verify_id_token(token)

            if self.verify_type == "REGISTER":
                user_phone = decoded_token.get('phone_number')

                if phone != user_phone:
                    self.raiseFailure("Firebase phone and register phone doesn't match.")

                if User.objects.filter(phone=user_phone).exists():
                    self.raiseFailure(self.phone_exists, self.phone_exists)

            return decoded_token
            
        except (auth.ExpiredIdTokenError, auth.InvalidIdTokenError, auth.RevokedIdTokenError) as e:
            # Handle authentication error
            self.raiseFailure(f"Firebase authentication error: {e}")

class VerifyAndRegisterMutation(mutations.Register):

    class Arguments:
        token = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, token=None, **kwargs):

        phone = kwargs.get('phone')
        email = kwargs.get('email')

        if phone:
            email and kwargs.pop('email')
            auth = VerifyToken("REGISTER")
            auth.verify(token, phone)
        elif email:
            # Delete the user if the user already exists and not verified.
            try:
                user = User.objects.get(email=email)
                if user.status.verified is False:
                    user.delete()
            except User.DoesNotExist:
                pass
        else:
            return GraphQLError("No Email or Phone.")

        response = super().mutate(root, info, **kwargs)

        # Mark the user as verified if it is from phone number
        if response.success and phone:
            user = User.objects.get(phone=phone)
            if user.status.verified is False:
                user.status.verified = True
                user.status.save(update_fields=["verified"])
                user_verified.send(sender=cls, user=user)

        return response

class ChangePasswordMutation(mutations.PasswordReset):

    @classmethod
    def mutate(cls, root, info, **kwargs):
        token = kwargs.pop("token")

        auth = VerifyToken("CHANGEPSW")
        user_decoded = auth.verify(token)

        try:
            user = User.objects.get(phone=user_decoded.get('phone_number'))
        except User.DoesNotExist:
            raise GraphQLError("User not found.")

        f = cls.form(user, kwargs)
        if f.is_valid():
            revoke_user_refresh_token(user)
            user = f.save()

            if user.status.verified is False:
                user.status.verified = True
                user.status.save(update_fields=["verified"])
                user_verified.send(sender=cls, user=user)

            return cls(success=True)
        return cls(success=False, errors=f.errors.get_json_data())

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

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

class UserCreationCheckQuery(graphene.ObjectType):

    user_check = graphene.Field(
        UserCreationCheckType,
        email=graphene.String(),
        phone=graphene.String(),
        password1=graphene.String(),
        password2=graphene.String(),
        username= graphene.String()
    )

    def resolve_user_check(self, info, username, password1, password2, email=None, phone=None):

        errors = []

        if email is None and phone is None:
            errors.append("No Email or Phone.")

        if email and User.objects.filter(email=email).exists():
            errors.append("User with this Email already exists.")

        if phone and User.objects.filter(phone=phone).exists():
            errors.append("User with this Phone already exists.")
            
        if User.objects.filter(username=username).exists():
            errors.append("A user with this username already exists.")

        if password1.lower() != password2.lower():
            errors.append("The two password fields didn’t match.")
        else:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors.append(f"Invalid password: {', '.join(e)}")

        if len(errors) == 0:
            return UserCreationCheckType(success=True)
        else:
            return UserCreationCheckType(success=False, errors=errors)
        
class AuthQuery(
    UserCreationCheckQuery,
    # UserQuery,
    MeQuery,
    graphene.ObjectType
):
    pass

        
        
