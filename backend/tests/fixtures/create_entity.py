import pytest
from entity.models.Entity import Entity

@pytest.fixture
def create_entity():

  def _create_entity(
    name="Test Entity",
    description="This is testing entity",
    type="School",
    verified=True,
    users=[]
  ):
    
    # Create a entity
    entity = Entity.objects.create(
      name=name,
      description=description,
      type=type,
      verified=verified
    )

    entity.users.set(users)

    return entity
  
  return _create_entity

