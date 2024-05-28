from django.core.management.base import BaseCommand

from post.models.Post import Post
from entity.models.Entity import Entity

# pipenv run python manage.py assign_entity_to_posts

class Command(BaseCommand):
  help = 'Assign entity to all posts'

  def handle(self, *args, **kwargs):
    # Fetch all PostFile objects
    entity = Entity.objects.get(id=1)
    updated_count = Post.objects.all().update(entity=entity)

    self.stdout.write(self.style.SUCCESS(f'Successfully assigned selfdive entity to {updated_count} posts'))