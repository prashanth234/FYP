import graphene
from graphql import GraphQLError

# Models
from core.models.Reward import Reward

# Type
from core.schema.type.RewardsType import RewardsType

# Authentications
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):

    rewards = graphene.List(RewardsType)

    @login_required
    def resolve_rewards(root, info):
        return Reward.objects.filter(external=True)