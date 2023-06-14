import graphene
from graphql import GraphQLError

# Models
from categories.models.Competition import Competition
from categories.models.Category import Category

# Schema
# from categories.schema.categorySchema import CategoryType

# Type
from categories.schema.type.CategoryType import CategoryType
from categories.schema.type.CompetitionType import CompetitionType


class CreateCompetitionMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        category = graphene.ID(required=True)
        description = graphene.String()
        last_date = graphene.Date(required=True)
        points = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    competition = graphene.Field(CompetitionType)

    @classmethod
    def mutate(cls, root, info, name, category, last_date, points, description=''):
        category = Category.objects.get(pk=category)
        competition = Competition(name=name, category=category, description=description, last_date=last_date, points=points)
        competition.save()
        return CreateCompetitionMutation(competition=competition)

class UpdateCompetitionMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)
        name = graphene.String()
        category = graphene.ID()
        description = graphene.String()
        last_date = graphene.Date(required=True)
        points = graphene.Int(required=True)


    # The class attributes define the response of the mutation
    competition = graphene.Field(CompetitionType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None, category=None, last_date=None, points=None):
        competition = Competition.objects.get(pk=id)

        if not competition:
            raise GraphQLError("Competition with this ID does not exist.")
        
        if category:
            competition.category = Category.objects.get(pk=category)
        
        if name:
            competition.name = name

        if description:
            competition.description = description

        if last_date:
            competition.last_date = last_date

        if points:
            competition.points = points

        competition.save()

        return UpdateCompetitionMutation(competition=competition)

class DeleteCompetitionMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        Competition.objects.get(pk=id).delete()
        return DeleteCompetitionMutation(success=True)

class Mutation(graphene.ObjectType):
    create_competition = CreateCompetitionMutation.Field()
    update_competition = UpdateCompetitionMutation.Field()
    delete_competition = DeleteCompetitionMutation.Field()

class Query(graphene.ObjectType):

    all_competitions = graphene.List(CompetitionType)

    def resolve_all_competitions(root, info):
        return Competition.objects.all()
    
    competition_details = graphene.Field(CompetitionType, id=graphene.Int())

    def resolve_competition_details(root, info, id):
        return Competition.objects.get(pk=id)