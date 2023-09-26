from django.contrib import admin

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition
from categories.models.Transaction import Transaction
from categories.models.Winner import Winner
from categories.models.Reward import Reward
from categories.models.Post import Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'last_date')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('status', 'user', 'created_at', 'points', 'type')

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'competition', 'post', 'won_by_likes', 'reward')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('position', 'points', 'type')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'competition', 'likes')

# admin.site.register(Competition)