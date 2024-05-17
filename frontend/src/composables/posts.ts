import { useLazyQuery, useQuery } from '@vue/apollo-composable'
import { InfiniteScrollCustomEvent } from '@ionic/vue'
import gql from 'graphql-tag'
import { ref, computed } from 'vue'

export function getQuery(type: string) {
  // Also update the create post and trending query and post details
  return {
    QUERY: gql`
      query ${type} ($category: ID, $competition: ID, $page: Int, $perPage: Int, $trending: Boolean, $cursor: String) {
        ${type} (category: $category, competition: $competition, page: $page, perPage: $perPage, trending: $trending, cursor: $cursor) @connection(key: "feed", filter: ["category", "competition", "trending"]) {
          posts {
            id,
            likes,
            userLiked,
            description,
            createdAt,
            isBot,
            postfileSet {
              files {
                lg,
                md,
                og
              },
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
            },
            ispublic
          },
          total
        }
      }
    `
  }
}

export function getPosts(
  type: string,
  category?: string,
  competition?: string
) {

  const variables = {
    competition: ref(competition),
    category: ref(category),
    trending: ref(false),
    page: 1,
    perPage: 4
  }

  const {QUERY: POST_QUERY} = getQuery(type)

  const { result: posts, loading, fetchMore, refetch } = useQuery(POST_QUERY, () => ({
    page: variables.page,
    perPage: variables.perPage,
    competition: variables.competition.value,
    category: variables.category.value,
    trending: variables.trending.value,
    cursor: undefined
  }))

  const fetchMoreCompleted = computed(() => {
    if (!posts.value) {
      return false
    }

    const postsFetched = posts.value[type].posts.length
    const totalPosts = posts.value[type].total

    return postsFetched >= totalPosts
  })

  function getMore(ev: InfiniteScrollCustomEvent) {

    if (fetchMoreCompleted.value) { return }

    const postsFetched = posts.value[type].posts.length
    const cursor = posts.value[type].posts[postsFetched-1].createdAt
    const page = Math.floor(postsFetched/variables.perPage) + 1
  
    return fetchMore({
      variables: {
        page,
        cursor
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        // No new feed posts
        if (!fetchMoreResult) return previousResult

        
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
    refetch,
    fetchMoreCompleted
  }
}

export function getWinners(competition: string | undefined) {
  const WINNERS_QUERY = gql`
    query winners ($competition: ID!) {
      winners (competition: $competition) {
        post {
          id,
          likes,
          userLiked,
          description,
          postfileSet {
            files {
              lg,
              md,
              og
            },
            width,
            height
          },
          user {
            id,
            username,
            avatar
          }
        },
        position,
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

export function getPostDetails(
  id: string,
  category: string
) {

  const QUERY = gql`
    query PostDetails ($id: ID!, $category: ID) {
      postDetails (id: $id, category: $category) {
        id,
        likes,
        userLiked,
        description,
        createdAt,
        isBot,
        postfileSet {
          files {
            lg,
            md,
            og
          },
          width,
          height
        },
        category {
          id,
          oftype
        },
        user {
          id,
          username,
          avatar
        },
        competition {
          expired
        }
      }
    }
  `

  const { result: post, loading, onResult, onError } = useQuery(QUERY, () => ({
    id,
    category
  }))

  return {
    post,
    loading,
    onResult,
    onError
  }
}

export function getTrending() {

  const TRENDING_QUERY = gql`
    query TrendingPosts ($competition: ID!) {
      trendingPosts (competition: $competition) {
        posts {
          id,
          likes,
          userLiked,
          description,
          createdAt,
          isBot,
          postfileSet {
            files {
              lg,
              md,
              og
            },
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
  `

  const variables = {
    competition: ref<string|undefined>('')
  }

  const { result, loading, refetch, onResult, load } = useLazyQuery(TRENDING_QUERY, () => ({
    competition: variables.competition.value,
  }))

  return {
    result,
    refetch,
    onResult,
    load,
    variables
  }
}