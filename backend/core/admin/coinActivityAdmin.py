from django.contrib import admin, messages
from django.contrib.contenttypes.models import ContentType

from core.models.CoinActivity import CoinActivity
from post.models.Post import Post
from categories.models.Competition import Competition

from django.urls import reverse
from django.utils.html import format_html

class CompetitionTypeFilter(admin.SimpleListFilter):
    title = 'Contest'
    parameter_name = 'content_type'

    def lookups(self, request, model_admin):
        competition = Competition.objects.all()
        return [(ct.id, ct.name) for ct in competition]

    def queryset(self, request, queryset):
        if self.value():
            posts_qs = queryset.filter(
                content_type=ContentType.objects.get_for_model(Post), 
                object_id__in=Post.objects.filter(competition=self.value()).values_list('id', flat=True)
            )
            return posts_qs
        return queryset
    
@admin.register(CoinActivity)
class CoinActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_link', 'points', 'type', 'status',)
    list_filter = ['type', 'status', CompetitionTypeFilter]

    def content_link(self, obj):
        # Generate a link to the related object's change page
        if obj.content_object:
            url = reverse(
                'admin:%s_%s_change' % (obj.content_type.app_label,  obj.content_type.model),
                args=[obj.object_id]
            )
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.content_object)
        return obj.content_object