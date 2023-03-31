# No need of resolve_all_categories if used with DjangoListField instad graphene.List
# all_categories = DjangoListField(CategoryType)
# allCategories {
#     name
# }
all_categories = graphene.List(CategoryType)

def resolve_all_categories(root, info):
    return Category.objects.all()
    # return Category.objects.all()

# categoryDetails (id:2) {
#     name
# }
category_details = graphene.Field(CategoryType, id=graphene.Int())

def resolve_category_details(root, info, id):
    return Category.objects.get(pk=id)

# {
#   allCategories {
#    name
#  }
#  categoryDetails (id:1) {
#    name
#  }
#  allCompetitions (categoryId: 1) {
#    name,
#    category {
#      name
#    }
#  }
# }

## Parameterized competitions
# query getCompetitions($id: Int = 1){
#  allCategories {
#    name
#  }
#  categoryDetails (id:$id) {
#    name
#  }
#  allCompetitions (categoryId: $id) {
#    name,
#    category {
#      name
#    }
#  }
# }


all_competitions = graphene.List(CompetitionType, categoryId=graphene.Int())

def resolve_all_competitions(root, info, categoryId):
    return Competition.objects.filter(category=categoryId)
    # return Competition.objects.all()

# Create Mutation
# mutation {
#  
#  createCategory (name:"new category") {
#    category {
#      name
#    } 
#  }
#  
# }

class CategoryMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        # Notice we return an instance of this mutation
        return CategoryMutation(category=category)

class Mutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()

# Update mutation
# mutation {
#  
#  createCategory (id:3, name:"new categor1y") {
#    category {
#      name
#    } 
#  }
# 
# }

class CategoryMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        # Notice we return an instance of this mutation
        return CategoryMutation(category=category)

class Mutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()

# query {
#   allCategories {
#     name,
#     description,
#     competitions {
#       name,
#       posts {
#         description,
#         files {
#           file
#         }
#       }
#     }  
#   }
# }


# Create User

mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "supersecretpassword",
    password2: "supersecretpassword",
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}

# To get id of the user last user created

query {
  users (last: 1){
    edges {
      node {
        id,
        username,
        email,
        isActive,
        archived,
        verified,
        secondaryEmail
      }
    }
  }
}

query {
  users (last: 1){
    edges {
      node {
        id,
        username,
        email,
        isActive,
        archived,
        verified,
        secondaryEmail
      }
    }
  }
}