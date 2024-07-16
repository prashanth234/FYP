from graphene_django import DjangoObjectType
import graphene
from helpers.urlType import ImageUrlType
from entity.schema.query.userEntityQuery import UserEntityCheck
from django.db.models import Count, Q

# Models
from categories.models.Competition import Competition
from entity.models.Entity import Entity
from post.models.Post import Post
from categories.models.Category import Category

# Type
from categories.schema.type.CompetitionType import CompetitionType

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
  id = graphene.String()
  name = graphene.String()
  count = graphene.Int(entity_id=graphene.ID())
  color = graphene.String()

class StatsType(graphene.ObjectType):
  id = graphene.String()
  users = graphene.Int()
  posts = graphene.Int()
  categories = graphene.List(CategoryStatType)

  def resolve_id(self, info):
    return self.id

  def resolve_users(self, info):
    return self.users.count()
  
  def resolve_posts(self, info):
    return Post.objects.filter(entity=self.id).count()
  
  def resolve_categories(self, info):
    top_categories = (Category.objects
                      .annotate(count=Count('post', filter=Q(post__entity_id=self.id)))
                      .values('id', 'name', 'color', 'count')
                      .order_by('-count')[:4])

    categories_stats = []

    for category in top_categories:
      category["id"] = f"{self.id}-{category['id']}"
      categories_stats.append(CategoryStatType(**category))
    
    return categories_stats

class EntityType(ImageUrlType, DjangoObjectType):

  stats = graphene.Field(StatsType)
  user_access = graphene.String()
  competitions = graphene.List(CompetitionType)

  def resolve_stats(self, info):
    return self
  
  def resolve_type(self, info):
    return (self.other_type if self.type == 'Others' else self.type)

  def resolve_user_access(self, info):
    return UserEntityCheck.get_status(info.context.user, self.id)

  def resolve_competitions(self, info):
    if self.ispublic or UserEntityCheck.has_access(info.context.user, self.id):
      return Competition.objects.filter(entity_id=self.id)
    else:
      return []

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
      "ispublic",
      "competitions"
    )
    convert_choices_to_enum = False