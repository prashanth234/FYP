import json
import pytest
import os
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile

from post.models.Post import Post


@pytest.mark.django_db
def test_create_post_mutation(authenticate, file_client_query, create_category):
    
    category = create_category()

    # Define the mutation
    mutation = """
    mutation CreatePost($file: Upload!, $category: ID!, $competition: ID, $description: String!) {
        createPost(file: $file, category: $category, competition: $competition, description: $description) {
            post {
                id
                likes
                userLiked
                description
                createdAt
                postfileSet {
                    files {
                        lg,
                        md,
                        og
                    },
                    width
                    height
                }
                user {
                    username
                    avatar
                    id
                }
                category {
                    oftype
                }
                competition {
                    expired
                }
                isBot
            }
            coinActivity {
                id
                points
                description
                status
                createdAt
            }
        }
    }
    """

    # Read the image file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(test_dir, "tajmahal.jpg")
    with open(file_path, "rb") as file:
        image_content = file.read()

    image = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')
    image1 = SimpleUploadedFile(name='test_image1.jpg', content=image_content, content_type='image/jpeg')

    # Set variables for the mutation
    variables = {
        "category": category.id,
        "competition": None,
        "description": "this is art"
    }

    # Check without client authentication
    executed = file_client_query(mutation, variables=variables, files={'file': image})
    response = json.loads(executed.content)

    assert 'errors' in response
    assert len(response['errors']) == 1
    assert response['errors'][0]['message'] == 'You do not have permission to perform this action'

    # Check post creation with authentication
    client, user, headers = authenticate()
    executed = file_client_query(mutation, variables=variables, files={'file': image1}, headers=headers)
    response = json.loads(executed.content)

    # Check if the post was created in the database
    created_post_id = response['data']['createPost']['post']['id']
    created_post = Post.objects.get(pk=created_post_id)

    post_files = created_post.postfile_set.all()

    # Loop through the files and remove files created
    for post_file in post_files:
        try:
            shutil.rmtree(os.path.dirname(post_file.file.path))
        except OSError as e:
            print(f"Error: {e.strerror}")
        
    assert created_post is not None

    # Check if the response contains the expected fields
    assert 'createPost' in response['data']
    assert 'post' in response['data']['createPost']
    assert 'coinActivity' in response['data']['createPost']
    assert response['data']['createPost']['post']['description'] == "this is art"

    