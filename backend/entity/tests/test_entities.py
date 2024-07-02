import json
import pytest

# Test you query using the client_query fixture
@pytest.mark.django_db
def test_fetch_entities(client_query):
  response = client_query(
      '''
        query Entities {
          entities {
            id,
            name,
            description,
            image,
            city, 
            type
          }
        }
      ''')

  content = json.loads(response.content)
  assert 'errors' not in content