import graphene
from graphene_django import DjangoObjectType

# Models
from categories.models.Category import Category
from categories.models.Competation import Competation

# Schema
from categories.schema.competationSchema import CompetationType

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "description")

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
    def mutate(cls, root, info, name, id, description='', type=''):
        category = Category.objects.get(pk=id)
        category.name = name
        category.description = description
        category.type = type
        category.save()
        # Notice we return an instance of this mutation
        return CategoryMutation(category=category)

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

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(root, info):
        return Category.objects.all()
    
    category_details = graphene.Field(CategoryType, id=graphene.Int())

    def resolve_category_details(root, info, id):
        return Category.objects.get(pk=id)

    all_category_competations = graphene.List(CompetationType, categoryId=graphene.Int())

    def resolve_all_category_competations(root, info, categoryId):
        return Competation.objects.filter(category=categoryId)