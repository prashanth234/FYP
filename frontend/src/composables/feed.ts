
import { computed, watch } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { getPosts } from '@/composables/posts'
import { PostType } from '@/utils/interfaces'
import { InfiniteScrollCustomEvent, RefresherCustomEvent } from '@ionic/vue'
import { DocumentNode } from 'graphql'
import { useQuery } from '@vue/apollo-composable'

interface WinnerPostType extends PostType {
  winner: {
    position: number,
    post: undefined
  }
}

export function watchRoute(QUERY: DocumentNode, store: any, id?: string, postid?: string) {
  const route = useRoute()

  const { result, onResult, onError } = useQuery(QUERY, () => ({
    id
  }))

  onResult(({data, loading}) => {
    if (!loading) {
      // When a post is created or when user is logged/logout, entity/category details are changed as a result onResult method is called and store is updated.
      // So making sure that store gets updated, only when current page is entity details page.
      // Store should only hold the current page details. If the store holds entity details while patching, patch will fail as __typename is only readonly
      if (route.params.id == id) {
        store.patchDetails(data)
      }
      store.loading = false
    }
  })
  
  onError(() => {
    store.loading = false
  })

  // When an opened page is opened again, page is not rendered again so need to watch router params to update the store
  watch(() => route.params.id, () => {
    if (route.name == store.routeName && route.params.id == id) {
      store.patchDetails(result.value)
      intailize()
    }
  })

  // When the router leaves the details page set default get category details and clear the category information store
  onBeforeRouteLeave(() => {
    store.details.name && store.$reset()
  })

  function intailize() {
    postid && store.hideSinglePost(false, postid)
  }

  // When page is loaded for the first time
  intailize()
  
  return {
    store
  }
}
  

export function feed(store: any, content: any, category?: string, entity?: string, competition?: string) {
  // Abstract method to get entity/category posts and competition posts
  const allPosts = getPosts(store.queryType, category, undefined, entity)
  const cPosts = getPosts('competitionPosts', undefined, competition, undefined, 'allposts', true)

  const isCompetition = computed(() => {
    return !!store.selectedComptn?.id
  })

  const posts = computed(() => {
    if (isCompetition.value) {
      return (cPosts.posts.value?.competitionPosts || {})
    } else {
      return (allPosts.posts.value?.[store.queryType] || {})
    }
  })

  function loadCompetitionType(value: string) {
    store.tabSelected = value
    cPosts.variables.cpType.value = value
  }

  function loadCompetition() {
    cPosts.variables.competition.value = store.selectedComptn?.id
    cPosts.load()
  }

  function cancelCompetition() {
    cPosts.variables.competition.value = undefined
    cPosts.posts.value = undefined
  }

  async function refetch(event: RefresherCustomEvent | null) {
    store.refreshing = true

    if (isCompetition.value) {
      await cPosts.refetch()
    } else {
      await allPosts.refetch()
    }
    
    event?.target && event.target.complete && event.target.complete()
    store.refreshing = false
  }

  function fetchMore(ev: InfiniteScrollCustomEvent) {
    if (isCompetition.value) {
      cPosts.getMore(ev, content)
    } else {
      allPosts.getMore(ev, content)
    }
  }

  return {
    // posts and competition related
    posts,
    fetchMoreCompleted: allPosts.fetchMoreCompleted,
    loadCompetitionType,
    loadCompetition,
    cancelCompetition,
    fetchMore,
    refetch
  }
}