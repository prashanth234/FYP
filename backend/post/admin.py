from django.contrib import admin

from post.models.Post import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'category', 'competition', 'likes', 'is_bot', 'created_at')
    list_filter = ['user', 'category', 'competition']
