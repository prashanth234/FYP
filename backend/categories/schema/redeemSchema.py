import graphene
from graphql import GraphQLError
from django.db import transaction

# Models
from categories.models.Redeem import Redeem

# Type
from categories.schema.type.RedeemType import RedeemType

# Authentication
from graphql_jwt.decorators import login_required


class CreateRedeemMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    redeem = graphene.Field(RedeemType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, points):
        user = info.context.user

        if points < 0:
            raise GraphQLError("Points can't be negative")
        
        if points > user.points:
            raise GraphQLError('Points should be less or equal to points you have earned')
        
        user.points -= points
        redeem = Redeem(user=info.context.user, points=points)
        redeem.save()
        user.save()

        return CreateRedeemMutation(redeem=redeem)

class UpdateRedeemMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    redeem = graphene.Field(RedeemType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id, points):
        user = info.context.user
        redeem = Redeem.objects.get(pk=id)

        if not redeem:
            raise GraphQLError("Redeem with this ID does not exist.")
        
        if points < 0:
            raise GraphQLError("Points can't be negative")
        
        if user.status == 'R':
            raise GraphQLError("Redeemed points can't be updated")
        
        userPoints = user.points + redeem.points
        
        if points > userPoints:
            raise GraphQLError('Points should be less or equal to points you have earned')
        
        userPoints -= points
        user.points = userPoints
        redeem.points = points
        redeem.save()
        user.save()
        
        # Notice we return an instance of this mutation
        return UpdateRedeemMutation(redeem=redeem)

class DeleteRedeemMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id):
        user = info.context.user
        redeem = Redeem.objects.get(pk=id)

        if not redeem:
            raise GraphQLError("Redeem with this ID does not exist.")

        if user.status == 'R':
            raise GraphQLError("Redeemed points can't be deleted")
        
        user.points += redeem.points
        
        redeem.delete()
        user.save()
        return DeleteRedeemMutation(success=True)

class Mutation(graphene.ObjectType):
    create_redeem = CreateRedeemMutation.Field()
    update_redeem = UpdateRedeemMutation.Field()
    delete_redeem = DeleteRedeemMutation.Field()

class Query(graphene.ObjectType):

    redemptions = graphene.List(RedeemType)

    @login_required
    def resolve_redemptions(root, info):
        return Redeem.objects.filter(user=info.context.user)