import json
import pytest
import os
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile

from post.models.Post import Post


@pytest.mark.django_db
def test_update_post_mutation(authenticate, file_client_query, create_post):

    post = create_post()

    # Define the mutation
    mutation = """
      mutation ($id: ID!, $file: Upload, $description: String) {
        updatePost(id: $id, file: $file, description: $description) {
          post {
            id
            description
            postfileSet {
              files {
                lg,
                md,
                og
              },
              width
              height
            }
          }
        }
      }
    """

    # Read the image file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(test_dir, "tajmahal.jpg")
    with open(file_path, "rb") as file:
        image_content = file.read()

    # image = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')
    image1 = SimpleUploadedFile(name='test_image1.jpg', content=image_content, content_type='image/jpeg')

    # Set variables for the mutation
    variables = {
        "id": post.id,
        "description": "this is artjk"
    }

    # Check without client authentication
    # executed = file_client_query(mutation, variables=variables, files={'file': image})
    # response = json.loads(executed.content)

    # assert 'errors' in response
    # assert len(response['errors']) == 1
    # assert response['errors'][0]['message'] == 'You do not have permission to perform this action'

    # Check post creation with authentication
    client, user, headers = authenticate()
    executed = file_client_query(mutation, variables=variables, files={'file': image1}, headers=headers)
    response = json.loads(executed.content)

    post_files = post.postfile_set.all()

    # Loop through the files and remove files created
    for post_file in post_files:
        try:
            shutil.rmtree(os.path.dirname(post_file.file.path))
        except OSError as e:
            print(f"Error: {e.strerror}")

    # Check if the response contains the expected fields
    assert 'updatePost' in response['data']
    assert 'post' in response['data']['updatePost']
    assert response['data']['updatePost']['post']['description'] == "this is artjk"

    