import graphene
import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from django.core.files.base import ContentFile
from datetime import datetime
from graphql_auth.models import UserStatus
from core.models.User import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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

class UpdateAccountMutation(graphene.Mutation):

    class Arguments:
        gender = graphene.String()
        firstName = graphene.String()
        lastName = graphene.String()
        dateOfBirth = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    user = graphene.Field(UserType)
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, gender=None, firstName=None, lastName=None, dateOfBirth=None, email=None, phone=None):
        
        user = info.context.user
        
        if user.status.verified and email:
            raise GraphQLError("Email can't be updated, please reachout to support", extensions={'status': 403})
        
        if email == "" and phone == "":
            raise GraphQLError("Please provide either email or phone number", extensions={'status': 400})
        
        if gender is not None:
            user.gender = gender

        if firstName is not None:
            user.first_name = firstName

        if lastName is not None:
            user.last_name = lastName

        if dateOfBirth:
            user.date_of_birth = dateOfBirth
        
        if email is not None:
            UserStatus.clean_email(email)
            user.email = email

        if phone is not None:
            if User.objects.filter(phone=phone).exists():
                raise GraphQLError("Phone number must be unique", extensions={'status': 400})
            user.phone = phone

        user.save()
        
        return UpdateAccountMutation(user=user, success=True)

class VerifyAndRegisterMutation(mutations.Register):

    class Arguments:
        token = graphene.String()

    @classmethod
    def registrationFailed(cls, message=None):
        raise GraphQLError(message or "Failed to register user.")
    
    @classmethod
    def mutate(cls, root, info, token=None, **kwargs):

        phone = kwargs.get('phone')

        if phone:
            
            if token is None:
                logger.error(f"Token not found while registering user with phone number.")
                cls.registrationFailed()
            
            try:
                # Verify the Firebase token using the Firebase SDK
                decoded_token = auth.verify_id_token(token)
                user_phone = decoded_token.get('phone_number')

                if phone != user_phone:
                    logger.error(f"Firebase phone and register phone doesn't match.")
                    cls.registrationFailed()

                if User.objects.filter(phone=user_phone).exists():
                    logger.error(f"User with this phone number already exits.")
                    cls.registrationFailed("User with this phone number already exits.")
                
            except (auth.ExpiredIdTokenError, auth.InvalidIdTokenError, auth.RevokedIdTokenError) as e:
                # Handle authentication error
                logger.error(f"Firebase authentication error: {e}")
                cls.registrationFailed()

        return super().mutate(root, info, **kwargs)

class AuthMutation(graphene.ObjectType):
    register = VerifyAndRegisterMutation.Field()
    # register = mutations.Register.Field()
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

class UserCreationCheckType(graphene.ObjectType):

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

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

        
        
