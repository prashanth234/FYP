import graphene
from core.models.User import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from core.schema.type.UserType import UserCreationCheckType
from django.contrib.auth.validators import UnicodeUsernameValidator


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
    else:
      validator = UnicodeUsernameValidator()

      try:
        validator(username)
      except ValidationError as e:
        # Also update message in UI code in register form
        errors.append("Username may only contain letters, numbers and special characters @, ., +, -, and _  without spaces.")

      if len(username) > 25:
          errors.append('Username must be 25 characters or fewer.')

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