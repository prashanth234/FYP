import pytest
from categories.models.Category import Category

@pytest.fixture
def create_category():

  def _create_category(
    name="Photography",
    description="This is photography interest",
    key="photography",
    oftype="IMAGETEXT"
  ):
    
    # Create a category
    category = Category.objects.create(
      name=name,
      description=description,
      key=key,
      oftype=oftype
    )

    return category
  
  return _create_category

