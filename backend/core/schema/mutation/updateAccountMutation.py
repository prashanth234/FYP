import graphene
from graphql import GraphQLError
from core.models.User import User
from graphql_auth.models import UserStatus

# Type
from core.schema.type.UserType import UserType

# Authentications
from graphql_jwt.decorators import login_required

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