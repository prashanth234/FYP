import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

# Models
from categories.models.Competation import Competation
from categories.models.Category import Category

# Schema
# from categories.schema.categorySchema import CategoryType

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "description")

class CompetationType(DjangoObjectType):
    class Meta:
        model = Competation
        fields = ("id", "name", "description", "category")

class CreateCompetationMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        category = graphene.ID(required=True)
        description = graphene.String()

    # The class attributes define the response of the mutation
    competation = graphene.Field(CompetationType)

    @classmethod
    def mutate(cls, root, info, name, category, description=''):
        category = Category.objects.get(pk=category)
        competation = Competation(name=name, category=category, description=description)
        competation.save()
        return CreateCompetationMutation(competation=competation)

class UpdateCompetationMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)
        name = graphene.String()
        category = graphene.ID()
        description = graphene.String()

    # The class attributes define the response of the mutation
    competation = graphene.Field(CompetationType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None, category=None):
        competation = Competation.objects.get(pk=id)

        if not competation:
            raise GraphQLError("Competation with this ID does not exist.")
        
        if category:
            competation.category = Category.objects.get(pk=category)
        
        if name:
            competation.name = name

        if description:
            competation.description = description

        competation.save()

        return UpdateCompetationMutation(competation=competation)

class DeleteCompetationMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        Competation.objects.get(pk=id).delete()
        return DeleteCompetationMutation(success=True)

class Mutation(graphene.ObjectType):
    create_competation = CreateCompetationMutation.Field()
    update_competation = UpdateCompetationMutation.Field()
    delete_competation = DeleteCompetationMutation.Field()

class Query(graphene.ObjectType):

    all_competations = graphene.List(CompetationType)

    def resolve_all_competations(root, info):
        return Competation.objects.all()
    
    competation_details = graphene.Field(CompetationType, id=graphene.Int())

    def resolve_competation_details(root, info, id):
        return Competation.objects.get(pk=id)