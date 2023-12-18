import graphene
from graphql import GraphQLError

# Models
from categories.models.Category import Category

# Type
from categories.schema.type.CategoryType import CategoryType

# Authentication
from graphql_jwt.decorators import login_required

import logging

logger = logging.getLogger(__name__)

class CreateCategoryMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        description = graphene.String()
        type = graphene.String()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, description='', type=''):
        category = Category(name=name, description=description, type=type)
        category.save()
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        description = graphene.String()
        type = graphene.String()
        id = graphene.ID()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None, type=None):
        category = Category.objects.get(pk=id)

        if not category:
            raise GraphQLError("Category with this ID does not exist.")
        
        if name:
            category.name = name
        
        if description:
            category.description = description
        
        if type:
            category.type = type

        category.save()
        # Notice we return an instance of this mutation
        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        Category.objects.get(pk=id).delete()
        return DeleteCategoryMutation(success=True)

class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()

class Query(graphene.ObjectType):

    categories = graphene.List(CategoryType)

    def resolve_categories(root, info):
#       logger.info('getting categories')
        return Category.objects.all().order_by('order')
    
    category_details = graphene.Field(CategoryType, id=graphene.Int())

    def resolve_category_details(root, info, id):
        return Category.objects.get(pk=id)

    # all_category_competitions = graphene.List(CompetitionType, categoryId=graphene.Int())

    # def resolve_all_category_competitions(root, info, categoryId):
    #     return Competition.objects.filter(category=categoryId)