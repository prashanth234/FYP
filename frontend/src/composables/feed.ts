
import { computed, watch } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { getPosts, getWinners, getTrending } from '@/composables/posts'
import { PostType, WinnerType } from '@/utils/interfaces'
import { InfiniteScrollCustomEvent, RefresherCustomEvent } from '@ionic/vue'

interface WinnerPostType extends PostType {
  winner: {
    position: number,
    post: undefined
  }
}

export function watchRoute(routeName: string, id?: string, postid?: string) {
  const route = useRoute()
  const store = useCategoryInfoStore()

  // When another category is opened after a category is opened, page is not rendered again so need to watch router params
  watch(() => route.params.id, () => {
    if (route.name == routeName && route.params.id == id) {
      intailize()
    }
  })

  // When the router leaves the details page set default get category details and clear the category information store
  onBeforeRouteLeave(() => {
    store.details.name && store.$reset()
  })

  // When page is loaded for the first time
  function intailize() {
    postid && store.hideSinglePost(false, postid)
    id && store.getCategoryInfo(id)
  }

  intailize()
  
  return {
    store
  }
}
  

export function feed(type: string, content: any, category?: string, entity?: string, competition?: string) {
  // Abstract method to get entity/category posts and competition posts
  const store = useCategoryInfoStore()
  const allPosts = getPosts(type, category, undefined, entity)
  const trendingPosts = getTrending()
  const winnerPosts = getWinners()

  const posts = computed(() => {

    if (store.tabSelected == 'allposts') {

      return (allPosts.posts.value?.allPosts || {})

    } else if (store.tabSelected == 'trending') {

      return (trendingPosts.posts.value?.trendingPosts || {})

    } else if (store.tabSelected == 'winners') {

      const posts: {posts: WinnerPostType[], total: number} = {posts: [], total: 3}

      winnerPosts.posts.value?.winners.forEach((winner: WinnerType) => {
        const post: WinnerPostType = {
          winner: {
            ...winner,
            post: undefined
          },
          ...winner.post,
        }
        posts.posts.push(post)
      })

      return posts

    }

    return {}
  })

  function loadCompetitionType(value: string) {
    store.tabSelected = value

    if (value == 'trending') {

      trendingPosts.variables.competition.value = store.selectedComptn?.id
      trendingPosts.load() || trendingPosts.refetch()

    } else if (value == 'winners') {

      winnerPosts.variables.competition.value = store.selectedComptn?.id
      winnerPosts.load() || winnerPosts.refetch()

    }
  }

  function loadCompetition() {
    allPosts.variables.competition.value = store.selectedComptn?.id
  }

  function cancelCompetition() {
    allPosts.variables.competition.value = undefined
  }

  async function refetch(event: RefresherCustomEvent | null) {
    store.refreshing = true
    if (store.tabSelected == 'trending') {
      await (trendingPosts.load() || trendingPosts.refetch())
    } else if (store.tabSelected == 'allposts') {
      await allPosts.refetch()
    }
    event?.target && event.target.complete && event.target.complete()
    store.refreshing = false
  }

  function fetchMore(ev: InfiniteScrollCustomEvent) {
    allPosts.getMore(ev, content)
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