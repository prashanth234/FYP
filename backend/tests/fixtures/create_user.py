import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def create_user():

  User = get_user_model()

  def _create_user(
    email="sample@selfdive.com",
    phone="+919999999999",
    password="try123"
  ):
    
    # Create a entity
    user = User.objects.create(
      email=email,
      phone=phone
    )

    user.set_password(password)
    user.save()

    return user
  
  return _create_user