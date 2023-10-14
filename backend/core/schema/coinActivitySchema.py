import graphene
from graphql import GraphQLError
from django.db import transaction

# Models
from core.models.CoinActivity import CoinActivity
from core.models.Reward import Reward

# Type
from core.schema.type.CoinActivityType import CoinActivitiesType

# Authentications
from graphql_jwt.decorators import login_required


class CreateCoinActivityMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        points = graphene.Int(required=True)
        reward = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    coinactivity = graphene.Field(CoinActivitiesType)
    userpoints = graphene.Int()

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, points, reward):
        user = info.context.user

        if points < 0:
            raise GraphQLError("Points can't be negative")
        
        if points > user.points:
            raise GraphQLError('Points should be less or equal to points you have earned')
        
        coinactivity = Reward.objects.get(pk=reward)
        user.points -= points
        coinactivity = CoinActivity(user=info.context.user, points=-points, type='REDEEM', content_object=coinactivity)
        coinactivity.save()
        user.save()

        return CreateCoinActivityMutation(coinactivity=coinactivity, userpoints=user.points)

class UpdateCoinActivityMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    coinactivity = graphene.Field(CoinActivitiesType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id, points):
        user = info.context.user
        coinactivity = CoinActivity.objects.get(pk=id)

        if not coinactivity:
            raise GraphQLError("CoinActivity with this ID does not exist.")
        
        if points < 0:
            raise GraphQLError("Points can't be negative")
        
        if user.status == 'R':
            raise GraphQLError("Redeemed points can't be updated")
        
        userPoints = user.points + coinactivity.points
        
        if points > userPoints:
            raise GraphQLError('Points should be less or equal to points you have earned')
        
        userPoints -= points
        user.points = userPoints
        coinactivity.points = points
        coinactivity.save()
        user.save()
        
        # Notice we return an instance of this mutation
        return UpdateCoinActivityMutation(coinactivity=coinactivity)

class DeleteCoinActivityMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()
    userpoints = graphene.Int()

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id):
        user = info.context.user
        coinactivity = CoinActivity.objects.get(pk=id)

        if not coinactivity:
            raise GraphQLError("CoinActivity with this ID does not exist.")

        if coinactivity.status != 'Q':
            raise GraphQLError("Reedem can't be canceled now")
        
        user.points -= coinactivity.points
        
        coinactivity.delete()
        user.save()
        return DeleteCoinActivityMutation(success=True, userpoints=user.points)

class Mutation(graphene.ObjectType):
    create_coinactivity = CreateCoinActivityMutation.Field()
    # update_coinactivity = UpdateCoinActivityMutation.Field()
    delete_coinactivity = DeleteCoinActivityMutation.Field()

class Query(graphene.ObjectType):

    coinactivities = graphene.List(CoinActivitiesType)

    @login_required
    def resolve_coinactivities(root, info):
        return CoinActivity.objects.filter(user=info.context.user).order_by('-pk')