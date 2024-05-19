from graphene_django import DjangoObjectType
import graphene
from entity.models.Entity import Entity
from post.models.Post import Post
from categories.models.Category import Category
from helpers.url_type import ImageUrlType
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
  count = graphene.Int()
  color = graphene.String()

class StatsType(graphene.ObjectType):
  users = graphene.Int()
  posts = graphene.Int()
  categories = graphene.List(CategoryStatType)

class EntityType(ImageUrlType, DjangoObjectType):

  stats = graphene.Field(StatsType)
  all_stats = graphene.Field(StatsType)
  user_access = graphene.String()

  def resolve_stats(self, info):
    posts = Post.objects.filter(entity=self.id)   
    stats = {
      "posts": posts.count(),
      "users": self.users.count()
    } 
    return StatsType(**stats)
  
  def resolve_all_stats(self, info):
    posts = Post.objects.filter(entity=self.id)
    categories = Category.objects.all()

    all_stats = {
      "posts": posts.count(),
      "users": self.users.count(),
      "categories": []
    }
    category_stat = {}

    for category in categories:
      category_stat["name"] = category.name
      category_stat["color"] = category.color
      category_stat["count"] = posts.filter(category=category).count()
      all_stats["categories"].append(CategoryStatType(**category_stat))
    
    return StatsType(**all_stats)
  
  def resolve_type(self, info):
    return dict(Entity.TYPE_CHOICES).get(self.type, None)

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
      "all_stats",
      "stats",
      "linkedin",
      "facebook",
      "instagram",
      "user_access",
      "ispublic"
    )
    convert_choices_to_enum = False