import { useQuery } from '@vue/apollo-composable'
import { IonInfiniteCustomEvent } from '@ionic/vue'
import gql from 'graphql-tag'
import { ref } from 'vue'

export function getPosts(type: string, competition: number | undefined, category: number | undefined) {

  const variables = {
    competition: ref(competition),
    category: ref(category),
    page: 1,
    perPage: 2
  }

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
            username,
            avatar
          }
        },
        total
      }
    }
  `

  // let page = 1
  // const variables1 = {
  //   page: 1,
  //   perPage: 1
  // }
  // if (category) {
  //   Object.assign(variables1, {category})
  // }
  // if (competition) {
  //   Object.assign(variables1, {competition})
  // }
  // const { result: posts, loading, fetchMore } = useQuery(POST_QUERY, () => (variables1))

  const { result: posts, loading, fetchMore, refetch } = useQuery(POST_QUERY, () => ({
    page: variables.page,
    perPage: variables.perPage,
    competition: variables.competition.value,
    category: variables.category.value
  }))

  function getMore(ev: IonInfiniteCustomEvent) {
    if (posts.value[type].posts.length >= posts.value[type].total) {
      ev.target.complete() 
      return 
    }
    
    variables.page++
  
    fetchMore({
      variables: {
        page: variables.page
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
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

  // watch(posts, (value) => {
  //   console.log(value)
  // })

  return {
    posts,
    loading,
    POST_QUERY,
    variables,
    getMore,
    refetch
  }
}