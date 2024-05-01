import json
import pytest

# Test you query using the client_query fixture
@pytest.mark.django_db
def test_fetch_categories(client_query):
    response = client_query(
        '''
        query {
            categories {
              id,
              name,
              description
            }
        }
        '''
    )

    content = json.loads(response.content)
    assert 'errors' not in content