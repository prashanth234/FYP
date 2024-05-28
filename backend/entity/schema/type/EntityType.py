from graphene_django import DjangoObjectType
import graphene
from entity.models.Entity import Entity
from post.models.Post import Post
from categories.models.Category import Category
from helpers.urlType import ImageUrlType
from entity.schema.query.userEntityQuery import UserEntityCheck

# Dynamic graphql fields
# def get_stats_dict():
#   stats = {
#     "users": graphene.Int(),
#     "posts": graphene.Int()
#   }

#   for category in Category.objects.all():
#     stats[category.key] = graphene.Int()

#   return stats

# StatsType = type('StatsType', (graphene.ObjectType,), get_stats_dict())

class CategoryStatType(graphene.ObjectType):
  name = graphene.String()
  count = graphene.Int(entity_id=graphene.ID())
  color = graphene.String()

class StatsType(graphene.ObjectType):
  users = graphene.Int()
  posts = graphene.Int()
  categories = graphene.List(CategoryStatType)

  def resolve_users(self, info):
    return self.users.count()
  
  def resolve_posts(self, info):
    return Post.objects.filter(entity=self.id).count()
  
  def resolve_categories(self, info):
    posts = Post.objects.filter(entity=self.id)
    categories = Category.objects.all()

    categories_stats = []
    category_stat = {}

    for category in categories:
      category_stat["name"] = category.name
      category_stat["color"] = category.color
      category_stat["count"] = posts.filter(category=category).count()
      categories_stats.append(CategoryStatType(**category_stat))
    
    return categories_stats

class EntityType(ImageUrlType, DjangoObjectType):

  stats = graphene.Field(StatsType)
  user_access = graphene.String()

  def resolve_stats(self, info):
    return self
  
  def resolve_type(self, info):
    return (self.other_type if self.type == 'Others' else self.type)

  def resolve_user_access(self, info):
    return UserEntityCheck.get_status(info.context.user, self.id)

  class Meta:
    model = Entity
    fields = (
      "id",
      "name",
      "description",
      "image",
      "city",
      "type",
      "stats",
      "linkedin",
      "facebook",
      "instagram",
      "user_access",
      "ispublic"
    )
    convert_choices_to_enum = False