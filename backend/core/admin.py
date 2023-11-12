from django.contrib import admin
from django.apps import apps
from core.models.User import User
from core.models.Support import Support
from core.models.CoinActivity import CoinActivity
from core.models.Reward import Reward
from core.models.Faq import Faq

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone') 
    search_fields = ('username',) 

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'description', 'comments', 'status')
    list_filter = ['status']

    def user_link(self, obj):
        # Generate a link to the related object's change page
        if obj.user:
            url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name),
                          args=[obj.user.id])
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.user)
        return '-'

@admin.register(CoinActivity)
class CoinActivityAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'user', 'points', 'type', 'content_type', 'content_link')
    list_filter = ['type', 'status']

    def content_link(self, obj):
        # Generate a link to the related object's change page
        if obj.content_object:
            url = reverse(
                'admin:%s_%s_change' % (obj.content_type.app_label,  obj.content_type.model),
                args=[obj.object_id]
            )
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.content_object)
        return obj.content_object

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'points', 'type', 'pointsvalue')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'order', 'type']

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)