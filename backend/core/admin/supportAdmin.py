from django.contrib import admin
from core.models.Support import Support

from django.urls import reverse
from django.utils.html import format_html

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('description', 'user_link', 'comments', 'status', 'created_at')
    list_filter = ['status', 'user']
    ordering = ('-created_at',)

    def user_link(self, obj):
        # Generate a link to the related object's change page
        if obj.user:
            url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name),
                          args=[obj.user.id])
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.user)
        return '-'