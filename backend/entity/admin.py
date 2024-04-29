from django.contrib import admin
from entity.models.Entity import Entity

# Register your models here.

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'phone', 'email', 'key', 'city', 'image',)