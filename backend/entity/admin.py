from django.contrib import admin
from entity.models.Entity import Entity
from entity.models.Verification import Verification

# Register your models here.

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
  list_display = ('user', 'entity', 'request')

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'phone', 'email', 'city', 'ispublic', 'verified')