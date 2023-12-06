from django.contrib import admin
from django import forms

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition
from categories.models.Winner import Winner
from categories.models.Post import Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'last_date', "points")

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'competition', 'post', 'won_by_likes', 'position', "points")
                    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'category', 'competition', 'likes', 'is_bot', 'created_at')
    list_filter = ['user', 'category', 'competition']

# admin.site.register(Competition)