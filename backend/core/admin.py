from django.contrib import admin
from django.apps import apps
from core.models.User import User
from core.models.Support import Support
from core.models.CoinActivity import CoinActivity
from core.models.Reward import Reward
from core.models.Faq import Faq

# Register your models here.
admin.site.register(User)

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('description', 'comments', 'status', 'contact', 'user')

@admin.register(CoinActivity)
class CoinActivityAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'user', 'points', 'type')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'points', 'type', 'pointsvalue')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'order', 'type']

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)