import graphene
from graphql import GraphQLError

# Models
from categories.models.Competition import Competition
from categories.models.Category import Category

# Schema
# from categories.schema.categorySchema import CategoryType

# Type
from categories.schema.type.CompetitionType import CompetitionType

from entity.schema.query.userEntityQuery import UserEntityCheck
from helpers.common import get_today_date

class CreateCompetitionMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        category = graphene.String(required=True)
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

class CompetitionList(graphene.ObjectType):
    global_list = graphene.List(CompetitionType)
    entity_list = graphene.List(CompetitionType)

class Query(graphene.ObjectType):

    all_competitions = graphene.List(CompetitionType)

    def resolve_all_competitions(root, info):
        return Competition.objects.all()
    
    competitions = graphene.Field(
        CompetitionList,
        category_id=graphene.ID(),
        entity_id=graphene.ID()
    )

    def resolve_competitions(root, info, category_id, entity_id):
        selfdive_entity = '1'
        entity_list = []

        competitions = Competition.objects.filter(category_id=category_id, last_date__gte=get_today_date())
        global_list = competitions.filter(entity_id=selfdive_entity)
        
        if selfdive_entity != entity_id and UserEntityCheck.has_access(info.context.user, entity_id):
            entity_list = competitions.filter(entity_id=entity_id)

        return CompetitionList(global_list=global_list, entity_list=entity_list)
    
    competition_details = graphene.Field(
        CompetitionType,
        id=graphene.ID(required=True)
    )

    def resolve_competition_details(root, info, id):
        return Competition.objects.get(pk=id)