import json
import pytest

@pytest.mark.django_db
def test_fetch_myposts(authenticate, client_query):
    client, user, headers = authenticate()

    response = client_query(
        '''
        query {
            myPosts {
              total,
              posts {
                description
              }
            }
        }
        ''',
        headers=headers
    )

    content = json.loads(response.content)
    assert 'errors' not in content