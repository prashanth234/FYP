import graphene
from graphql import GraphQLError
from django.db import transaction

# Models
from categories.models.Transaction import Transaction

# Type
from categories.schema.type.TransactionsType import TransactionsType

# Authentications
from graphql_jwt.decorators import login_required


class CreateTransactionMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    ctransaction = graphene.Field(TransactionsType)
    userpoints = graphene.Int()

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
        ctransaction = Transaction(user=info.context.user, points=points, type='REDEEM')
        ctransaction.save()
        user.save()

        return CreateTransactionMutation(ctransaction=ctransaction, userpoints=user.points)

class UpdateTransactionMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    ctransaction = graphene.Field(TransactionsType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id, points):
        user = info.context.user
        ctransaction = Transaction.objects.get(pk=id)

        if not ctransaction:
            raise GraphQLError("Transaction with this ID does not exist.")
        
        if points < 0:
            raise GraphQLError("Points can't be negative")
        
        if user.status == 'R':
            raise GraphQLError("Redeemed points can't be updated")
        
        userPoints = user.points + ctransaction.points
        
        if points > userPoints:
            raise GraphQLError('Points should be less or equal to points you have earned')
        
        userPoints -= points
        user.points = userPoints
        ctransaction.points = points
        ctransaction.save()
        user.save()
        
        # Notice we return an instance of this mutation
        return UpdateTransactionMutation(ctransaction=ctransaction)

class DeleteTransactionMutation(graphene.Mutation):
    
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
        ctransaction = Transaction.objects.get(pk=id)

        if not ctransaction:
            raise GraphQLError("Transaction with this ID does not exist.")

        if ctransaction.status != 'Q':
            raise GraphQLError("Transaction can't be canceled now")
        
        user.points += ctransaction.points
        
        ctransaction.delete()
        user.save()
        return DeleteTransactionMutation(success=True, userpoints=user.points)

class Mutation(graphene.ObjectType):
    create_transaction = CreateTransactionMutation.Field()
    # update_transaction = UpdateTransactionMutation.Field()
    delete_transaction = DeleteTransactionMutation.Field()

class Query(graphene.ObjectType):

    transactions = graphene.List(TransactionsType)

    @login_required
    def resolve_transactions(root, info):
        return Transaction.objects.filter(user=info.context.user).order_by('-pk')