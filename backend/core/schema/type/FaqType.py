from graphene_django import DjangoObjectType
from core.models.Faq import Faq

class FaqType(DjangoObjectType):
    class Meta:
        model = Faq
        fields = ("question", "answer")