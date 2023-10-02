import { useQuery } from '@vue/apollo-composable'
import { InfiniteScrollCustomEvent } from '@ionic/vue'
import gql from 'graphql-tag'
import { ref } from 'vue'

export function getPosts(
  type: string,
  competition: string | undefined, 
  category: string | undefined
) {

  const variables = {
    competition: ref(competition),
    category: ref(category),
    trending: ref(false),
    page: 1,
    perPage: 5
  }

  // Also update create post query
  const POST_QUERY = gql`
    query ${type} ($category: Int, $competition: Int, $page: Int, $perPage: Int, $trending: Boolean, $cursor: Int) {
      ${type} (category: $category, competition: $competition, page: $page, perPage: $perPage, trending: $trending, cursor: $cursor) @connection(key: "feed", filter: ["category", "competition", "trending"]) {
        posts {
          id,
          likes,
          userLiked,
          description,
          postfileSet {
            file
          },
          user {
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
  `

  const { result: posts, loading, fetchMore, refetch } = useQuery(POST_QUERY, () => ({
    page: variables.page,
    perPage: variables.perPage,
    competition: variables.competition.value,
    category: variables.category.value,
    trending: variables.trending.value,
    cursor: undefined
  }))

  function getMore(ev: InfiniteScrollCustomEvent) {

    if (!posts.value) {
      ev.target.complete()
      return
    }

    const postsFetched = posts.value[type].posts.length
    const totalPosts = posts.value[type].total

    if (postsFetched >= totalPosts) {
      ev.target.complete() 
      return 
    }

    const cursor = posts.value[type].posts[postsFetched-1].id
    const page = Math.floor(postsFetched/variables.perPage) + 1
  
    fetchMore({
      variables: {
        page,
        cursor
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
            ],
            total: fetchMoreResult[type].total
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

export function getWinners(competition: string | undefined) {
  const WINNERS_QUERY = gql`
    query winners ($competition: Int) {
      winners (competition: $competition) {
        post {
          id,
          likes,
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
        reward {
          position
        },
        wonByLikes
      }
    }
  `

  const { result: winners, loading, refetch, onResult } = useQuery(WINNERS_QUERY, () => ({
    competition
  }))

  return {
    winners,
    refetch,
    onResult
  }
}