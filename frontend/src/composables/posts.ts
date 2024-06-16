import { useLazyQuery, useQuery } from '@vue/apollo-composable'
import { InfiniteScrollCustomEvent } from '@ionic/vue'
import gql from 'graphql-tag'
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

export const POST_COMMON_FIELDS = `
  id,
  likes,
  userLiked,
  description,
  createdAt,
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
  }
`

export function getQuery(type: string) {
  // This is common query can be use for allPosts, myPosts and entityPosts Queries

  if (type == 'entityPosts') {
    return {
      QUERY: gql`
        query ${type} (
          $entity: ID!,
          $competition: ID,
          $perPage: Int,
          $cursor: String
        ) {
          ${type} (
            entity: $entity,
            competition: $competition,
            perPage: $perPage,
            cursor: $cursor
          ) @connection(key: "entity-feed", filter: ["entity", "competition"]) {
            posts {
              ${POST_COMMON_FIELDS}
            },
            total
          }
        }
      `
    }
  } else if (type == 'allPosts') {
    return {
      QUERY: gql`
        query ${type} (
          $category: ID!,
          $competition: ID,
          $perPage: Int,
          $cursor: String
        ) {
          ${type} (
            category: $category,
            competition: $competition,
            perPage: $perPage,
            cursor: $cursor
          ) @connection(key: "feed", filter: ["category", "competition"]) {
            posts {
              ${POST_COMMON_FIELDS},
              isBot
            },
            total
          }
        }
      `
    }
  } else {
    // Return myPosts query
    return {
      QUERY: gql`
        query ${type} (
          $category: ID,
          $competition: ID,
          $perPage: Int,
          $cursor: String
        ) {
          ${type} (
            category: $category,
            competition: $competition,
            perPage: $perPage,
            cursor: $cursor
          ) @connection(key: "myposts", filter: ["category", "competition"]) {
            posts {
              ${POST_COMMON_FIELDS},
              competition {
                expired
              }
            },
            total
          }
        }
      `
    }
  }
}

export function getPosts(
  type: string,
  category?: string,
  competition?: string,
  entity?: string
) {

  const PER_PAGE = 4
  const MAX_POSTS_WITHOUT_LOGIN = 8
  const CHECK_MAX_POSTS = type != 'myPosts'

  const variables = {
    competition: ref(competition),
    category: ref(category),
    entity: ref(entity),
    perPage: PER_PAGE
  }

  const {QUERY: POST_QUERY} = getQuery(type)
  const user = useUserStore()
  const auth = useAuthStore()

  const queryVariables = () => ({
    category: variables.category.value,
    competition: variables.competition.value,
    entity: variables.entity.value,
    perPage: variables.perPage,
    cursor: undefined
  })

  const { result: posts, loading, fetchMore, refetch } = useQuery(POST_QUERY, queryVariables)

  const fetchMoreCompleted = computed(() => {
    if (!posts.value) {
      return false
    }

    const postsFetched = posts.value[type].posts.length
    const totalPosts = posts.value[type].total

    return postsFetched >= totalPosts
  })

  function getMore(ev: InfiniteScrollCustomEvent, content: any) {

    if (fetchMoreCompleted.value || !posts.value) { 
      ev.target.complete()
      return 
    }

    // Show max of MAX_POSTS_WITHOUT_LOGIN post if user is not authenticated and ask user to login/register
    if (
      CHECK_MAX_POSTS &&
      !user.success &&
      posts.value[type].total > MAX_POSTS_WITHOUT_LOGIN &&
      posts.value[type].posts.length >= MAX_POSTS_WITHOUT_LOGIN
    ) {
      auth.open()
      auth.showMessage('Take your journey further! Log in to reveal more posts.', 'info')
      // scrollByPoint should be always higher than threshold
      content && (content.value && content.value.$el.scrollByPoint(0, -50, 500))
      setTimeout(() => { ev.target.complete() }, 100)
      return
    }

    const postsFetched = posts.value[type].posts.length
    const cursor = posts.value[type].posts[postsFetched-1].createdAt
    const page = Math.floor(postsFetched/variables.perPage) + 1
  
    return fetchMore({
      variables: {
        cursor
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        // Finish the infinate event
        setTimeout(() => { ev.target.complete() }, 100)

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

export function getWinners(competition?: string | undefined) {
  const WINNERS_QUERY = gql`
    query winners ($competition: ID!) {
      winners (competition: $competition) {
        post {
          ${POST_COMMON_FIELDS}
        },
        position,
        wonByLikes
      }
    }
  `

  const variables = {
    competition: ref<string|undefined>(competition)
  }

  const { result: posts, loading, refetch, onResult, load } = useLazyQuery(WINNERS_QUERY, () => ({
    competition: variables.competition.value
  }))

  return {
    posts,
    refetch,
    onResult,
    load,
    variables
  }
}

export function getPostDetails(
  id: string,
  category: string | undefined,
  entity: string | undefined
) {

  const QUERY = gql`
    query PostDetails ($id: ID!, $category: ID, $entity: ID) {
      postDetails (id: $id, category: $category, entity: $entity) {
        ${POST_COMMON_FIELDS}
      }
    }
  `

  const { result: post, loading, onResult, onError } = useQuery(QUERY, () => ({
    id,
    entity,
    category
  }))

  return {
    post,
    loading,
    onResult,
    onError
  }
}

export function getTrending(competition?: string | undefined) {

  const TRENDING_QUERY = gql`
    query TrendingPosts ($competition: ID!) {
      trendingPosts (competition: $competition) {
        posts {
          ${POST_COMMON_FIELDS}
        },
        total
      }
    }
  `

  const variables = {
    competition: ref<string|undefined>(competition)
  }

  const { result: posts, loading, refetch, onResult, load } = useLazyQuery(TRENDING_QUERY, () => ({
    competition: variables.competition.value,
  }))

  return {
    posts,
    refetch,
    onResult,
    load,
    variables
  }
}