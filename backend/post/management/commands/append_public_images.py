from django.core.management.base import BaseCommand

from categories.models.Category import Category
from categories.models.Competition import Competition
from core.models.Reward import Reward
from post.models.Post import PostFile
from core.models.User import User

# python manage.py append_public_images

class Command(BaseCommand):
  help = 'Update /public for all models which has file'

  def update_public(self, instances):
    for instance in instances:
      if instance.image and not instance.image.name.startswith('public/'):
        instance.image.name = 'public/' + instance.image.name
        instance.save()
  
  def update_public_file(self, instances):
    for instance in instances:
      if instance.file and not instance.file.name.startswith('public/'):
        instance.file.name = 'public/' + instance.file.name
        instance.save()

  def update_public_avatar(self, instances):
    for instance in instances:
      if instance.avatar and not instance.avatar.name.startswith('public/'):
        instance.avatar.name = 'public/' + instance.avatar.name
        instance.save()

  def handle(self, *args, **kwargs):
    # Fetch all PostFile objects
    self.update_public_file(PostFile.objects.all())
    self.update_public(Category.objects.all())
    self.update_public(Competition.objects.all())
    self.update_public(Reward.objects.all())
    self.update_public_avatar(User.objects.all())

    self.stdout.write(self.style.SUCCESS('Successfully appended "public/" to the field values.'))