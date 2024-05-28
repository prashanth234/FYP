from django.core.management.base import BaseCommand

from core.models.User import User
from entity.models.Entity import Entity

# pipenv run python manage.py add_users_to_entity

class Command(BaseCommand):
  help = 'Add all users to selfdive entity'

  def handle(self, *args, **kwargs):
    users = User.objects.all()
    entity = Entity.objects.get(id=1)
    entity.users.add(*users)

    self.stdout.write(self.style.SUCCESS(f'Successfully added {users.count()} users to selfdive entity'))