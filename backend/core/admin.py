from django.contrib import admin
from django.apps import apps
from core.models.User import User
from core.models.Support import Support

# Register your models here.
admin.site.register(User)

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('description', 'comments', 'status', 'contact', 'user')

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)