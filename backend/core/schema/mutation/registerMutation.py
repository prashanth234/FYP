from authentication.utils import revoke_user_refresh_token
from authentication.signals import user_verified
from graphql import GraphQLError
from core.models.User import User
import graphene
from authentication import mutations

# Firebase
from firebase_admin import auth

import logging

logger = logging.getLogger(__name__)

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