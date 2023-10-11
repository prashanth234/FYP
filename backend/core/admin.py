from django.contrib import admin
from django.apps import apps
from core.models.User import User
from core.models.Support import Support
from core.models.Transaction import Transaction
from core.models.Reward import Reward

# Register your models here.
admin.site.register(User)

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('description', 'comments', 'status', 'contact', 'user')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('status', 'user', 'created_at', 'points', 'type')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'position', 'points', 'type', 'external')

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)