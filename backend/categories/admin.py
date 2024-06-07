from django.contrib import admin
from django import forms

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition
from categories.models.Winner import Winner

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'last_date', "points")

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    fields = ['post', 'won_by_likes', 'position', 'points']
    list_display = ('user', 'competition', 'post', 'won_by_likes', 'points', 'position')
    list_filter = ['competition']

# admin.site.register(Competition)