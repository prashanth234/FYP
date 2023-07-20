from django.contrib import admin

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'last_date', 'points')

# admin.site.register(Competition)