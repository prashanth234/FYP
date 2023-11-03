import graphene

# Type
from core.schema.type.FaqType import FaqType

# Model
from core.models.Faq import Faq


class Query(graphene.ObjectType):

    faqs = graphene.List(FaqType, qtype=graphene.String())

    def resolve_faqs(root, info, qtype='REWARD'):
        return Faq.objects.filter(type=qtype).order_by('order')