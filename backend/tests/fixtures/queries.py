from graphene_django.utils.testing import graphql_query
from graphene_file_upload.django.testing import file_graphql_query
import pytest

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func

@pytest.fixture
def file_client_query(client):
    def func(*args, **kwargs):
        return file_graphql_query(*args, **kwargs, client=client)
    
    return func