<template>
  <ion-page>
    <ion-content class="full-height" ref="content">

      <ion-grid>

        <ion-row>

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" :class="{'post-col': posts?.allPosts?.total > 5}" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row class="ion-justify-content-center">

              <!-- Information about category -->
              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11" >

                <ion-card class="ion-padding border-radius-std ion-no-margin" >

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

              <!-- Heading -->
              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11">
                <div class="feed">
                  <div class="title">Feed</div>
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
                  <ion-card-content class="ion-text-center" style="font-weight: 500;">
                    The contest has concluded! Please take a look at our other ongoing contests.
                  </ion-card-content>
                </ion-card>

                <ion-card
                  class="note-card"
                  color="light"
                  v-else-if="state.tabSelected == 'trending'"
                >
                  <ion-card-content>
                    <div class="ion-text-center" style="font-weight: 600;" v-if="!posts?.allPosts?.posts.length">
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
                v-if="state.pdShow"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
              >
                <post :post="state.pdetails"/>
                <div class="ion-margin-vertical ion-text-center ion-padding-vertical">
                  <ion-button fill="clear" @click="hidePostDetails(false)">Click to discover more posts</ion-button>
                </div>
              </ion-col>

              <!-- Display the posts -->
              <ion-col
                v-show="state.tabSelected != 'winners' && !state.pdShow"
                size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8"
                v-for="(post, index) in posts?.allPosts?.posts"
                :key="post.id"
              >
                <post :post="post"></post>
              </ion-col>

              <!-- Display winners -->
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

            <ion-infinite-scroll :disabled="state.pdShow" @ionInfinite="fetchMore" threshold="0">
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
import { reactive, watch, ref } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { IonButton, IonPage, IonCard, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, SegmentValue, IonCardContent, InfiniteScrollCustomEvent, useIonRouter } from '@ionic/vue'

import Post from '@/components/PostContainer.vue'
import Competitions from '@/components/CompetitionsContainer.vue'
import { getPosts, getWinners, getPostDetails } from '@/composables/posts'
import { scrollTop } from '@/composables/scroll'

import { CompetitionInfo } from '@/mixims/interfaces'
import { Post as PostType } from '@/mixims/interfaces'

import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
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
  pdetails: PostType | null
}

const state: State = reactive({
  competition: null,
  creatingPost: false,
  refreshCreatePost: 1,
  tabSelected: 'allposts',
  winners: [],
  pdShow: false,
  pdetails: null
})

const route = useRoute();
const categoryInfo = useCategoryInfoStore();
const user = useUserStore();
const toast = useToastStore();
const ionRouter = useIonRouter();

const props = defineProps({
  id: String,
  postid: String
})

// As opened category details page are opened again need to update the categorydetails since
// once the category details is opened it will not get rerendered again
watch(() => route.params.id, () => {
  if (route.name == 'CategoryDetails' && route.params.id == props.id) {
    categoryInfo.getCategoryInfo(props.id, ionRouter)
  }
})

// When the router leaves the details page set default get category details and clear the category information store
onBeforeRouteLeave(() => {
  setCategoryDefault()
  categoryInfo.name && categoryInfo.$reset()
  props.postid && (state.pdShow = true)
})

props.postid && fetchPostDetails(props.postid, props.id || '')

props.id && categoryInfo.getCategoryInfo(props.id, ionRouter)

const { content } = scrollTop()

const category =  props.id || undefined
const { posts, getMore, variables } = getPosts('allPosts', category)

function loadCompetitionPosts(competition: CompetitionInfo) {
  hidePostDetails(true)
  state.tabSelected = 'allposts'
  categoryInfo.selectedComptn = competition
  variables.competition.value = competition.id
}

function setCategoryDefault() {
  if (!variables.competition.value) { return }
  variables.competition.value = undefined
  variables.trending.value = false
  categoryInfo.selectedComptn = null
  state.tabSelected = 'allposts'
}

function tabChanged(value: string) {
  state.tabSelected = value
  variables.trending.value = value == 'trending'

  if (value == 'winners') {
    state.winners = []
    const { onResult } = getWinners(categoryInfo.selectedComptn?.id)
    onResult(({data, loading}) => {
      !loading && (state.winners = data.winners)
    })
  }
}

function fetchMore(ev: InfiniteScrollCustomEvent) {
  if (user.success || posts.value?.allPosts.total <= 5) {
    getMore(ev)
  } else {
    // To see more post, ask user to login
    // toast.$patch({message: 'Take your journey further! Log in to reveal more posts.', color: 'primary', open: true})
    user.auth = true
    user.authMessage = 'Take your journey further! Log in to reveal more posts.'
    ev.target.complete()
    content.value && content.value.$el.scrollByPoint(0, -50, 500);
    // Commented this code because because on login posts are refetched and cache is cleard, if call for more posts then coflicts may occur.
    // const stopWatch = watch(user, () => {
    //   if (user.success) {
    //     getMore(ev)
    //   }
    //   stopWatch()
    // })
  }

}

// Get indivual post details if searched using url
function fetchPostDetails (id: string, category: string) {
  if (id && category) {
    state.pdetails = null
    const { onResult, onError } = getPostDetails(id, category)
    onResult(({data, loading}) => {
      if (!loading) {
        state.pdetails = data.postDetails
        hidePostDetails(false)
      }
    })
    onError((error) => {
      if (error?.graphQLErrors) {
        toast.$patch({message: error?.graphQLErrors[0].message, color: 'danger', open: true})
      } else {
        toast.$patch({message: 'Post retrieval error. Please Retry.', color: 'danger', open: true})
      }
      ionRouter.replace(`/interests/${props.id}/posts`)
    })
  }
}

function hidePostDetails (value: boolean) {
  state.pdShow = !value
}
</script>

<style scoped lang="scss">
.posts ion-card {
  margin-left: 0px;
  margin-right: 0px;
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
    font-weight: 600;
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
    font-weight: 600;
    line-height: 1.6;
  }
  .description {
    color: var(--ion-color-dark-tint);
  }
}
.feed {
  padding: 5px;
  .title {
    font-size: 18px;
    font-weight: 600;
    display: inline;
  }
}
</style>