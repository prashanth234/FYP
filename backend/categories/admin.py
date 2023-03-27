from django.contrib import admin

# Register your models here.
from categories.models.Category import Category
from categories.models.Post import Post
from categories.models.Competation import Competation

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Competation)
