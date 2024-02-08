from locust import HttpUser, task, between
from random import randint
import json

class WebsiteUser(HttpUser):
  wait_time = between(1, 5)

  @task
  def view_categories(self):
    query = """
              query {
                  categories {
                    id,
                    name,
                    description
                  }
              }
            """
    
    response = self.client.post(
      f'graphql', 
      json={'query': query},
      name='Get Categories')
    
    if response.status_code != 200:
      print(f"Request failed with status code: {response.status_code}")
      print(response.text)

  @task
  def view_posts(self):
    query = """
            query allPosts ($category: Int, $competition: Int, $page: Int, $perPage: Int, $trending: Boolean, $cursor: String) {
              allPosts (category: $category, competition: $competition, page: $page, perPage: $perPage, trending: $trending, cursor: $cursor) {
                posts {
                  id,
                  likes,
                  userLiked,
                  description,
                  createdAt,
                  isBot,
                  postfileSet {
                    file,
                    width,
                    height
                  },
                  user {
                    id,
                    username,
                    avatar
                  },
                  category {
                    oftype
                  },
                  competition {
                    expired
                  }
                },
                total
              }
            }
          """
    
    category_id = randint(1,8)
    cursor_id = randint(5, 29)
    variables = {"category": category_id, "cursor": cursor_id}
    
    payload = {
      "query": query,
      "variables": variables
    }

    response = self.client.post(
      f'graphql', 
      json=payload,
      name='Get Posts')
    
    if response.status_code == 200:
      # print(len(response.text.data.allPosts.posts))
      data = json.loads(response.text)
      print(len(data['data']['allPosts']['posts']))
    else:
      print(f"Request failed with status code: {response.status_code}")
      print(response.text)