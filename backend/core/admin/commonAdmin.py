from django.contrib import admin
from django.apps import apps
from core.models.User import User
from core.models.Reward import Reward
from core.models.Faq import Faq

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone') 
    search_fields = ('username',)

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'points', 'type', 'pointsvalue')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'order', 'type']

app = apps.get_app_config('authentication')

for model_name, model in app.models.items():
    admin.site.register(model)