import graphene

# Models
from core.models.Support import Support

class SupportMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        description = graphene.String(required=True)
        contact = graphene.String()

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, description, contact=None):
        if info.context.user.is_authenticated:
            support = Support(description=description, user=info.context.user)
        else:
            support = Support(description=description, contact=contact)
        
        support.save()
        return SupportMutation(success=True)

class Mutation(graphene.ObjectType):
    create_support = SupportMutation.Field()