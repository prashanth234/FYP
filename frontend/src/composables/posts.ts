import { useQuery } from '@vue/apollo-composable'
import { IonInfiniteCustomEvent } from '@ionic/vue'
import gql from 'graphql-tag'
import { watch } from 'vue'

export function getPosts(type: string, competition: number = 0, category: number = 0) {

  const POST_QUERY = gql`
    query ($category: Int, $competition: Int, $page: Int, $perPage: Int) {
      ${type} (category: $category, competition: $competition, page: $page, perPage: $perPage) {
        posts {
          id, 
          likeCount,
          userLiked,
          description,
          postfileSet {
            file
          },
          user {
            username
          }
        },
        total
      }
    }
  `
  
  let page = 1
  const variables = {
    page: 1,
    perPage: 1
  }

  if (category) {
    Object.assign(variables, {category})
  }

  if (competition) {
    Object.assign(variables, {competition})
  }


  const { result: posts, loading, fetchMore } = useQuery(POST_QUERY, () => (variables))

  function getMore(ev: IonInfiniteCustomEvent) {
    if (posts.value[type].posts.length == posts.value[type].total) {
      ev.target.complete() 
      return 
    }
  
    page++
  
    fetchMore({
      variables: {
        page: page
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        console.log("hello")
        // No new feed posts
        if (!fetchMoreResult) return previousResult

        // Complete infinate loading event
        ev.target.complete()
  
        // Concat previous feed with new feed posts
        return {
          ...previousResult,
          [type]: {
            ...previousResult[type],
            posts: [
              ...previousResult[type].posts,
              ...fetchMoreResult[type].posts
            ]
          }
        }
      },
    })
  }

  watch(posts, (value) => {
    console.log(value)
  })

  return {
    posts,
    loading,
    getMore,
    POST_QUERY,
    variables
  }
}