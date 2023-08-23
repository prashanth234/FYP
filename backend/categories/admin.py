from django.contrib import admin

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition
from categories.models.Redeem import Redeem
from categories.models.Winner import Winner

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'last_date', 'points')

@admin.register(Redeem)
class RedeemAdmin(admin.ModelAdmin):
    list_display = ('status', 'user', 'created_at', 'points')

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'post', 'likes')

# admin.site.register(Competition)