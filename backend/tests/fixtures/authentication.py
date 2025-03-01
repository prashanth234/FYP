from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from datetime import datetime
import pytest


@pytest.fixture
def authenticate(client):
    def do_authenticate(is_staff=False):
      user_model = get_user_model()
      user = user_model.objects.create_user(id=1000000, username='testuser', email='test@gmail.com', created_at=datetime.now(), is_staff=is_staff)
      client.force_login(user)
      token = get_token(user)
      headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
      return client, user, headers
    return do_authenticate
