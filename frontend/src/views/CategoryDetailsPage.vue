<template>
  <ion-page>
    <ion-content class="full-height">

      <ion-grid>

        <ion-row>

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" :class="{'post-col': posts?.allPosts?.total > 5}" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row class="ion-justify-content-center">

              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11" >

                <ion-card class="ion-padding border-radius-std ion-no-margin" color="light">

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
                  @close-competition="goBackCategory()"
                  @select-competition="loadCompetitionPosts"
                  :vertical="false"
                />
              </ion-col>

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

              <ion-col
                class="ion-no-padding"
                size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11"
              >

                <ion-card
                  class="competition-note"
                  color="light"
                  v-if="categoryInfo.selectedComptn?.expired"
                >
                  <ion-card-content class="ion-text-center" style="font-weight: 500;">
                    The contest has concluded! Please take a look at our other ongoing contests.
                  </ion-card-content>
                </ion-card>

                <ion-card
                  class="competition-note"
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

              <!-- Display the posts -->
              <ion-col
                v-show="state.tabSelected != 'winners'"
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
                <post :post="winner.post" :reward="winner.reward">
                </post>
              </ion-col>

            </ion-row>

            <ion-infinite-scroll @ionInfinite="getMore" threshold="0">
              <ion-infinite-scroll-content loading-text="Loading..." loading-spinner="bubbles"></ion-infinite-scroll-content>
            </ion-infinite-scroll>

          </ion-col>

          <!-- Competitions for large screens -->
          <ion-col class="ion-hide-md-down" size="4" size-xs="12" size-sm="12" size-md="4" size-lg="4" size-xl="4">
            <competitions
              @select-competition="loadCompetitionPosts"
              @close-competition="goBackCategory()"
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
import { onBeforeRouteLeave, useRoute, } from 'vue-router'
import { IonButton, IonPage, IonCard, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, SegmentValue, IonCardContent } from '@ionic/vue'
import Post from '@/components/PostContainer.vue'
import { getPosts, getWinners } from '@/composables/posts'
import { CompetitionInfo } from '@/mixims/interfaces'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import Competitions from '@/components/CompetitionsContainer.vue'
import { Post as PostType } from '@/mixims/interfaces'

interface Winner {
  post: PostType,
  wonByLikes: number,
  reward: {
    position: number
  }
}

interface State {
  competition: CompetitionInfo | null,
  refreshCreatePost: number,
  creatingPost: Boolean,
  tabSelected: SegmentValue | undefined,
  winners: Array<Winner>
}

const state: State = reactive({
  competition: null,
  creatingPost: false,
  refreshCreatePost: 1,
  tabSelected: 'allposts',
  winners: []
})

const route = useRoute();
const categoryInfo = useCategoryInfoStore();

const props = defineProps({
  id: String
})

watch(() => route.params.id, () => {
  if (route.name == 'CategoryDetails' && route.params.id == props.id) {
    categoryInfo.getCategoryInfo(props.id)
  }
})

// const hasTrendingPosts = computed(() => {
//   return state.tabSelected == 'trending' && posts.value?.allPosts?.posts.length
// })

onBeforeRouteLeave(() => {
  goBackCategory()
  categoryInfo.name && categoryInfo.$reset()
})

props.id && categoryInfo.getCategoryInfo(props.id)

const category =  props.id || undefined
const { posts, getMore, variables } = getPosts('allPosts', undefined, category)

function loadCompetitionPosts(competition: CompetitionInfo) {
  state.tabSelected = 'allposts'
  categoryInfo.selectedComptn = competition
  variables.competition.value = competition.id
}

function goBackCategory() {
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

</script>

<style scoped>
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
.competition-note {
  /* background-color: #e8f4f8; */
  box-shadow: none;
  color: var(--ion-color-dark);
  margin-left: 10px !important;
  margin-right: 10px !important;
}
</style>