<template>
  <ion-page>
    <ion-content class="full-height" ref="content">

      <ion-refresher slot="fixed" @ionRefresh="refreshPosts($event)">
        <ion-refresher-content
          :pulling-icon="chevronDownCircleOutline"
          pulling-text="Pull to refresh"
          refreshing-spinner="circles"
          refreshing-text="Refreshing..."
        >
        </ion-refresher-content>
      </ion-refresher>

      <ion-grid>

        <ion-row>

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" :class="{'post-col': posts?.allPosts?.total > 5}" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row class="ion-justify-content-center">

              <!-- Information about category -->
              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11" >

                <ion-card style="min-height: 100px;" class="ion-padding border-radius-std ion-no-margin" >

                  <div class="title category">
                    {{ categoryInfo.name }}
                  </div>

                  <div class="description category">
                    {{ categoryInfo.description }}
                  </div>
                  
                </ion-card>

              </ion-col>

              <!-- Competitions for small screens -->
              <ion-col size="12" class="ion-hide-md-up" style="padding-bottom: 0px;">
                <competitions
                  @close-competition="setCategoryDefault()"
                  @select-competition="loadCompetitionPosts"
                  :vertical="false"
                />
              </ion-col>

              <!-- Feed Heading -->
              <ion-col size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11">
                <div class="feed">

                  <div class="title">
                    Feed
                  </div>

                  <Refresh
                    @refresh="refreshPosts(null)"
                    :refreshing="state.refreshing"
                  />
                  
                  <div style="margin-left: auto;">
                    <ion-button
                      v-if="categoryInfo.selectedComptn && !categoryInfo.selectedComptn.expired"
                      :disabled="state.tabSelected == 'trending'"
                      @click="tabChanged('trending')"
                      style="margin-left: 15px;"
                      class="close-button"
                      size="small"
                      shape="round"
                      color="light"
                    >
                      Trending
                    </ion-button>
                    <ion-button
                      v-if="categoryInfo.selectedComptn && categoryInfo.selectedComptn.expired"
                      :disabled="state.tabSelected == 'winners'"
                      @click="tabChanged('winners')"
                      style="margin-left: 15px;"
                      class="close-button"
                      size="small"
                      shape="round"
                      color="light"
                    >
                      Winners
                    </ion-button>
                    <ion-button
                      v-if="categoryInfo.selectedComptn"
                      :disabled="!categoryInfo.selectedComptn || state.tabSelected == 'allposts'"
                      @click="tabChanged('allposts')"
                      class="close-button"
                      size="small"
                      shape="round"
                      color="light"
                    >
                      All
                    </ion-button>
                  </div>
                </div>
              </ion-col>

              <!-- Notes -->
              <ion-col
                class="ion-no-padding"
                size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11"
              >

                <ion-card
                  class="note-card"
                  color="light"
                  v-if="categoryInfo.selectedComptn?.expired"
                >
                  <ion-card-content class="ion-text-center note-msg">
                    The contest has concluded! Please take a look at our other ongoing contests.
                  </ion-card-content>
                </ion-card>

                <ion-card
                  class="note-card"
                  color="light"
                  v-else-if="state.tabSelected == 'trending'"
                >
                  <ion-card-content class="note-msg">
                    <div class="ion-text-center" v-if="!trendingPosts?.trendingPosts?.posts.length">
                      Can't spot any trending posts? Be the one who sparks a new wave!<br>Unlock the path to trendiness with just 5 likes for your post!
                    </div>
                    <div v-else>
                      Contest's top 5 posts with at least 5 likes are currently trending here!
                    </div>
                  </ion-card-content>
                </ion-card>

              </ion-col>

              <!-- Single post -->
              <ion-col
                v-if="state.pdShow && props.postid"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
              >
                <SinglePost
                  :id="props.postid"
                  :category="props.id"
                  @more="hidePostDetails(true)"
                />
              </ion-col>

              <!-- Display the posts -->
              <ion-col
                v-show="state.tabSelected == 'allposts' && !state.pdShow"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
                v-for="post in posts?.allPosts?.posts"
                :key="post.id"
              >
                <post :post="post"></post>
              </ion-col>

              <!-- Display Trending -->
              <ion-col
                v-show="state.tabSelected == 'trending'"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
                v-for="(post, index) in trendingPosts?.trendingPosts?.posts" 
                :key="index"
              >
                <post :post="post"></post>
              </ion-col>

              <!-- Display Winners -->
              <ion-col
                v-show="state.tabSelected == 'winners'"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
                v-for="(winner, index) in state.winners" 
                :key="index"
              >
                <post :post="winner.post" :position="winner.position">
                </post>
              </ion-col>

            </ion-row>

            <ion-infinite-scroll 
              :disabled="state.pdShow || fetchMoreCompleted"
              :key="`${fetchMoreCompleted}`"
              @ionInfinite="fetchMore"
              :threshold="user.success ? '400px' : '30px'"
            >
              <ion-infinite-scroll-content loading-text="Loading..." loading-spinner="bubbles"></ion-infinite-scroll-content>
            </ion-infinite-scroll>

          </ion-col>

          <!-- Competitions for large screens -->
          <ion-col class="ion-hide-md-down" size="4" size-xs="12" size-sm="12" size-md="4" size-lg="4" size-xl="4">
            <competitions
              @select-competition="loadCompetitionPosts"
              @close-competition="setCategoryDefault()"
              :vertical="true"
            />
          </ion-col>

        </ion-row>

      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { RefresherCustomEvent, IonRefresher, IonRefresherContent, IonButton, IonPage, IonCard, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, SegmentValue, IonCardContent, InfiniteScrollCustomEvent, useIonRouter } from '@ionic/vue'
import { chevronDownCircleOutline } from 'ionicons/icons'

import Post from '@/components/PostContainer.vue'
import SinglePost from '@/components/SinglePostContainer.vue'
import Competitions from '@/components/CompetitionsContainer.vue'
import Refresh from '@/components/RefreshContainer.vue'
import { getPosts, getWinners, getTrending } from '@/composables/posts'
import { scrollTop } from '@/composables/scroll'

import { CompetitionInfo } from '@/utils/interfaces'
import { Post as PostType } from '@/utils/interfaces'

import { useUserStore } from '@/stores/user'
import { useCategoryInfoStore } from '@/stores/categoryInfo'

interface Winner {
  post: PostType,
  wonByLikes: number,
  position: number
}

interface State {
  competition: CompetitionInfo | null,
  refreshCreatePost: number,
  creatingPost: Boolean,
  tabSelected: SegmentValue | undefined,
  winners: Array<Winner>,
  pdShow: boolean,
  refreshing: boolean
}

const state: State = reactive({
  competition: null,
  creatingPost: false,
  refreshCreatePost: 1,
  tabSelected: 'allposts',
  winners: [],
  // pdshow is for showing single post details
  pdShow: false,
  refreshing: false
})

const route = useRoute();
const categoryInfo = useCategoryInfoStore();
const user = useUserStore();
const ionRouter = useIonRouter();

const props = defineProps({
  id: String,
  postid: String
})

// When another category is opened after a category is opened, page is not rendered again so need to watch router params
watch(() => route.params.id, () => {
  if (route.name == 'CategoryDetails' && route.params.id == props.id) {
    categoryInfo.getCategoryInfo(props.id, ionRouter)
  }
})

// When the router leaves the details page set default get category details and clear the category information store
onBeforeRouteLeave(() => {
  setCategoryDefault()
  categoryInfo.name && categoryInfo.$reset()
  props.postid && hidePostDetails(false)
})

props.postid && hidePostDetails(false)
props.id && categoryInfo.getCategoryInfo(props.id, ionRouter)

const { content } = scrollTop()

const category =  props.id || undefined
const { posts, getMore, variables, refetch, fetchMoreCompleted } = getPosts('allPosts', category)
const { variables: trendingVars, refetch: refetchTrending, load: loadTrending, result: trendingPosts } = getTrending()

function loadCompetitionPosts(competition: CompetitionInfo) {
  hidePostDetails(true)
  state.tabSelected = 'allposts'
  categoryInfo.selectedComptn = competition
  variables.competition.value = competition.id
}

function setCategoryDefault() {
  if (!variables.competition.value) { return }
  variables.competition.value = undefined
  categoryInfo.selectedComptn = null
  state.tabSelected = 'allposts'
}

async function refreshPosts(event: RefresherCustomEvent | null) {
  state.refreshing = true
  if (state.tabSelected == 'trending') {
    await refetchTrending()
  } else if (state.tabSelected == 'allposts') {
    await refetch()
  }
  event?.target && event.target.complete && event.target.complete()
  state.refreshing = false
}

function tabChanged(value: string) {
  state.tabSelected = value

  if (value == 'winners') {
    state.winners = []
    const { onResult } = getWinners(categoryInfo.selectedComptn?.id)
    onResult(({data, loading}) => {
      !loading && (state.winners = data.winners)
    })
  } else if (value == 'trending') {
    trendingVars.competition.value = categoryInfo.selectedComptn?.id
    loadTrending() || refetchTrending()
  }
}

function fetchMore(ev: InfiniteScrollCustomEvent) {
  getMore(ev, content)
}

function hidePostDetails (value: boolean) {
  state.pdShow = !value
}
</script>

<style scoped lang="scss">
.posts {
  padding: 2px;
  ion-card {
    margin-left: 0px;
    margin-right: 0px;
  }
}
ion-content::part(scroll) {
  padding-top: 0px;
}
ion-grid {
  --ion-grid-padding: 0px;
  --ion-grid-column-padding: 8px;
}
.post-col {
  min-height: 100vh;
}
.close-button {
  float: right;
  margin: 0px;
}
.category {
  &.title {
    color: var(--ion-color-dark);
    font-size: 19px;
    font-weight: 580;
    text-transform: uppercase;
    line-height: 1.8;
  }
  &.description {
    color: var(--ion-color-dark-tint);
  }
}
.competition {
  border-left: 4px solid var(--ion-color-light-shade);
  padding-left: 7px;
  margin-top: 20px;

  .title {
    color: var(--ion-color-dark);
    font-size: 17px;
    font-weight: 580;
    line-height: 1.6;
  }
  .description {
    color: var(--ion-color-dark-tint);
  }
}

@media only screen and (max-width: 576px) {
	// For small screens
  .category {
    &.title {
      font-size: 19px;
    }
  }
}
</style>