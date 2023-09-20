import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Transaction import Transaction


class TransactionsType(DjangoObjectType):

    class Meta:
        model = Transaction
        fields = ("id", "status", "points", "created_at", "type")