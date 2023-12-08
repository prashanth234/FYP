import graphene
from graphql import GraphQLError
from django.core.paginator import Paginator
from graphene_file_upload.scalars import Upload
from graphene_django.filter import DjangoFilterConnectionField
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import dateparse
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
import os


# Models
from categories.models.Competition import Competition
from categories.models.Category import Category
from categories.models.Post import Post, PostFile
from core.models.CoinActivity import CoinActivity

# Type
from categories.schema.type.PostType import PostType
from core.schema.type.CoinActivityType import CoinActivitiesType

# Authentications
from graphql_jwt.decorators import login_required


class CreatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        description = graphene.String()
        category = graphene.ID()
        competition = graphene.ID()
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)
    coin_activity = graphene.Field(CoinActivitiesType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, file=None, description='', category=None, competition=None):
        
        if not category and not competition:
            raise GraphQLError("Almost there! To continue, kindly pick your interest.", extensions={'status': 404})

        if competition:
            competition = Competition.objects.get(pk=competition)

            if competition.is_expired:
                raise GraphQLError("The contest has concluded! Please take a look at our other ongoing contests.", extensions={'status': 405})
            
            if Post.objects.filter(competition=competition, user=info.context.user).exists():
                raise GraphQLError("To maintain fairness, kindly note that each user is permitted only one post per contest.", extensions={'status': 405})
            
            category = competition.category
        elif category:
            category = Category.objects.get(pk=category)

        user = info.context.user

        post = Post(
            user=user,
            description=description,
            category=category,
            competition=competition or None
        )
        
        post.save()

        coinactivity = None

        if competition:
            ca_description = f'{competition.name} Contest - Participation Reward'
            coinactivity = CoinActivity(
                type='COMPPARTN',
                user=user,
                points=settings.COMPPARTN_POINTS,
                description=ca_description,
                content_object=post,
                status='Q'
            )
            coinactivity.save()

        if file:
            postFile = PostFile(
                post=post
            )

            filetype = file.content_type.split('/')[1]
            filename = f"posts/user_{info.context.user.id}/post_{post.id}.{filetype}"
            file_content = ContentFile(file.read())

            # Save the updated file with the new filename
            postFile.file.save(filename, file_content, save=False)

            postFile.save()

        return CreatePostMutation(post=post, coin_activity=coinactivity)
    
class UpdatePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)
        description = graphene.String()
        file = Upload()


    # The class attributes define the response of the mutation
    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, file=None, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        try:
            post = Post.objects.get(pk=id, user=info.context.user)
            if post.competition and post.competition.is_expired:
                raise GraphQLError("You can't delete or edit posts in closed contests to ensure fairness and transparency. Thanks for understanding!", extensions={'status': 405})
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")
        
        if description != None:
            post.description = description

        post.save()

        if file and post.category.oftype != 'TEXT':
            postFile = PostFile.objects.get(post=post)

            filetype = file.content_type.split('/')[1]
            filename = f"posts/user_{info.context.user.id}/post_{post.id}.{filetype}"
            file_content = ContentFile(file.read())
            original_filename = postFile.file.name

            # Save the updated file with the new filename
            postFile.file.save(filename, file_content)

            # Remove the existing file if it exists
            if original_filename:
                file_path = os.path.join(settings.MEDIA_ROOT, original_filename)
                if os.path.exists(file_path):
                    os.remove(file_path)


        return UpdatePostMutation(post=post)

class DeletePostMutation(graphene.Mutation):
    
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID(required=True)


    # The class attributes define the response of the mutation
    success = graphene.Boolean()
    ca_id = graphene.ID()

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(cls, root, info, id):

        ca_id = None
        
        try:
            post = Post.objects.get(pk=id, user=info.context.user)
            if post.competition and post.competition.is_expired:
                raise GraphQLError("You can't delete or edit posts in closed contests to ensure fairness and transparency. Thanks for understanding! ")
        except Post.DoesNotExist:
            raise GraphQLError("Post with logged in user does not exist.")
        
        try:
            postFile = PostFile.objects.get(post=post)
            postFile.file.storage.delete(postFile.file.name)
        except PostFile.DoesNotExist:
            pass

        if post.competition:
            try:
                content_type = ContentType.objects.get_for_model(Post)
                coinactivity = CoinActivity.objects.get(object_id=id, content_type=content_type)
                ca_id = coinactivity.id
                coinactivity.delete()
            except CoinActivity.DoesNotExist:
                pass

        post.delete()

        return DeletePostMutation(success=True, ca_id=ca_id)
    
class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()

class PostListType(graphene.ObjectType):
    posts = graphene.List(PostType)
    total = graphene.Int()

class AllPostsQuery(graphene.ObjectType):

    all_posts = graphene.Field(
        PostListType,
        category= graphene.Int(),
        competition=graphene.Int(),
        page=graphene.Int(),
        per_page=graphene.Int(),
        trending=graphene.Boolean(),
        cursor=graphene.String()
    )

    def resolve_all_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False, cursor=None):

        # If trending flag is set return top number of posts
        # if trending:
        #     top_posts = Post.objects.filter(likes__gte=5, competition=competition).order_by('-likes', 'created_at')[:5]
        #     return PostListType(posts=top_posts, total=len(top_posts))

        if competition:
            queryset = Post.objects.filter(competition=competition).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category).order_by('-created_at')
        else:
            raise GraphQLError("Interest or Contest not found.")
            # queryset = Post.objects.all().order_by('-pk')

        # paginator = Paginator(queryset, per_page)
        # page_obj = paginator.page(page)
        # posts = page_obj.object_list

        total = queryset.count()
        
        if cursor:
           if cursor.isdigit():
            queryset = queryset.filter(pk__lt=cursor)
           else:
            queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)

class MyPostsQuery(graphene.ObjectType):

    my_posts = graphene.Field(
        PostListType,
        category= graphene.Int(),
        competition=graphene.Int(),
        page=graphene.Int(),
        per_page=graphene.Int(),
        trending=graphene.Boolean(),
        cursor=graphene.String()
    )
    
    def resolve_my_posts(root, info, category=None, competition=None, page=1, per_page=10, trending=False, cursor=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("User not authenticated")
        
        if competition:
            queryset = Post.objects.filter(competition=competition, user=info.context.user).order_by('-created_at')
        elif category:
            queryset = Post.objects.filter(category=category, user=info.context.user).order_by('-created_at')
        else:
            queryset = Post.objects.filter(user=info.context.user).order_by('-created_at')
        
        # paginator = Paginator(queryset, per_page)
        # page_obj = paginator.page(page)
        # posts = page_obj.object_list

        total = queryset.count()
        
        if cursor:
           queryset = queryset.filter(created_at__lt=dateparse.parse_datetime(cursor))
        
        posts = queryset[:per_page]

        # Return paginated list of posts
        return PostListType(posts=posts, total=total)
    
class PostDetailsQuery(graphene.ObjectType):
    post_details = graphene.Field(PostType, id=graphene.String(), category=graphene.String())

    def resolve_post_details(root, info, id, category):
        return Post.objects.get(pk=id, category__id=category)

class TrendingPostsQuery(graphene.ObjectType):

    trending_posts = graphene.Field(
        PostListType,
        competition=graphene.Int(required=True)
    )

    def resolve_trending_posts(root, info, competition=None):
        top_posts = Post.objects.filter(likes__gte=5, competition=competition).order_by('-likes', 'created_at')[:5]
        return PostListType(posts=top_posts, total=len(top_posts))
    
class Query(
    AllPostsQuery,
    MyPostsQuery,
    PostDetailsQuery,
    TrendingPostsQuery,
    graphene.ObjectType):
    pass

    
    

    
    
        