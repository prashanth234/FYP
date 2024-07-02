import pytest
from post.models.Post import Post, PostFile
from core.models.User import User

@pytest.fixture
def create_post(authenticate, create_category, create_entity):

  def _create_post(
    description="This is photography interest"
  ):
    
    category = create_category()
    entity = create_entity()
    # user = User.objects.get(pk=1000000)
    client, user, headers = authenticate()
    
    # Create a post
    post = Post(
      user=user,
      description=description,
      category=category,
      entity=entity
    )

    post.save()

    postfile = PostFile(
      post=post,
      width=400,
      height=400
    )

    postfile.save()

    return post
  
  return _create_post

