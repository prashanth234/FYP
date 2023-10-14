from django.contrib import admin
from django import forms

# Register your models here.
from categories.models.Category import Category
from categories.models.Competition import Competition
from categories.models.Winner import Winner
from categories.models.Post import Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'oftype', 'key', 'image')

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'last_date', "points")

class WinnerForm(forms.ModelForm):
    class Meta:
        model = Winner
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the selected "Competition" instance from the form data
        selected_competition = self.instance.competition if self.instance else None
        if selected_competition:
            # Filter the "Post" field queryset based on the selected "Competition"
            self.fields['post'].queryset = self.instance.post.all()

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    # form = WinnerForm
    list_display = ('id', 'user', 'competition', 'post', 'won_by_likes', 'position', "points")
                    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "post":
    #         selected_competition_id = request.GET.get('competition', None)
    #         if selected_competition_id:
    #             kwargs["queryset"] = Post.objects.filter(competition=selected_competition_id)
    #         else:
    #         # Filter the category choices based on the 'featured' field
    #             kwargs["queryset"] = Post.objects.all()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'competition', 'likes')

# admin.site.register(Competition)