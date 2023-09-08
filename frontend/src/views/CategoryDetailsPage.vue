<template>
  <ion-page>
    <ion-content class="full-height">

      <ion-grid>

        <ion-row>

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" :class="{'post-col': posts?.allPosts?.total > 5}" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row class="ion-justify-content-center">

              <!-- Breadcrumb for navigation from category to competition -->
              <!-- <ion-col size="12" class="ion-no-padding">

                <ion-breadcrumbs color="primary">
                  <ion-breadcrumb class="cpointer" @click="goBackCategory()">
                    {{ categoryInfo.name }}
                    <ion-icon slot="separator" style="margin-top: 5px" :icon="arrowForward"></ion-icon>
                  </ion-breadcrumb>
                  <ion-breadcrumb v-if="categoryInfo.selectedComptn">{{ categoryInfo.selectedComptn.name }}</ion-breadcrumb>
                  <ion-icon style="margin-top: 7px;" v-if="categoryInfo.selectedComptn" @click="goBackCategory()" class="close-icon ml-auto cpointer" size="large" :icon="closeOutline"></ion-icon>
                </ion-breadcrumbs>

              </ion-col> -->

              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11" >

                <ion-card class="ion-padding border-radius-std ion-no-margin" color="light">

                  <div class="title category">
                    {{ categoryInfo.name }}
                  </div>

                  <div class="description category">
                    {{ categoryInfo.description }}
                  </div>

                  <!-- <div v-if="categoryInfo.selectedComptn" class="competition">
                    <div class="title">
                      {{ categoryInfo.selectedComptn.name }}
                      <ion-button class="close-button" @click="goBackCategory()" size="small" shape="round" color="light">Close</ion-button>
                    </div>

                    <div class="description">
                      {{ categoryInfo.selectedComptn.description }}
                    </div>
                  </div> -->
                  
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

              <!-- Competition details -->
              <!-- <ion-col size="12" v-if="categoryInfo.selectedComptn">
                <competition-details />
              </ion-col> -->

              <!-- Create Post -->
              <!-- <ion-col size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8" v-if="!categoryInfo.loading">
                <create-post
                  :fixed-preview-height="false"
                  :key="state.refreshCreatePost"
                  :creatingPost="state.creatingPost"
                  @uploadPost="createNewPost"
                  type="create"
                >
                </create-post>
              </ion-col> -->

              <!-- Toggle between all posts and top 5 -->
              <!-- <ion-col size="12" v-if="categoryInfo.selectedComptn">
                <ion-segment :value="state.tabSelected" @ionChange="tabChanged">
                  <ion-segment-button value="allposts">
                    <ion-label>All Posts</ion-label>
                  </ion-segment-button>
                  <ion-segment-button value="trending">
                    <ion-label>Top 5</ion-label>
                  </ion-segment-button>
                </ion-segment>
              </ion-col> -->

              <ion-col size="10" size-xs="12" size-sm="12" size-md="11" size-lg="11" size-xl="11">
                <div class="feed">
                  <div class="title">Feed</div>
                  <ion-button
                    v-if="categoryInfo.selectedComptn"
                    :disabled="state.tabSelected == 'trending'"
                    @click="tabChanged('trending')"
                    style="margin-left: 15px;"
                    class="close-button"
                    size="small"
                    shape="round"
                    color="light"
                  >
                    Top 5
                  </ion-button>
                  <ion-button
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

              

              <!-- Display the posts -->
              <ion-col size="9" size-xs="12" size-sm="10" size-md="8" size-lg="8" size-xl="8" v-for="(post, index) in posts?.allPosts?.posts" :key="post.id">
                <post :post="post"></post>
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
import gql from 'graphql-tag'
import { IonButton, IonPage, IonCard, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonBreadcrumb, IonBreadcrumbs, IonSegment, IonSegmentButton, SegmentCustomEvent, SegmentValue } from '@ionic/vue'
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { getPosts } from '@/composables/posts'
import { UpdatePostVariables, CompetitionInfo } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'
import { arrowForward, closeOutline, radio } from 'ionicons/icons'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import Competitions from '@/components/CompetitionsContainer.vue'
import CompetitionDetails from '@/components/CompetitionInfoContainer.vue'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

interface State {
  competition: CompetitionInfo | null,
  refreshCreatePost: number,
  creatingPost: Boolean,
  tabSelected: SegmentValue | undefined
}

const state: State = reactive({
  competition: null,
  creatingPost: false,
  refreshCreatePost: 1,
  tabSelected: 'allposts'
})

const toast = useToastStore();
const user = useUserStore();
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

onBeforeRouteLeave(() => {
  goBackCategory()
  categoryInfo.name && categoryInfo.$reset()
})

props.id && categoryInfo.getCategoryInfo(props.id)

const category =  props.id ? parseInt(props.id) : undefined
const { POST_QUERY, posts, loading, getMore, refetch, variables } = getPosts('allPosts', undefined, category)

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
}

function createNewPost(createVariables: UpdatePostVariables) {

  if (!user.success) {
    user.auth = true
    return
  }

  state.creatingPost = true

  let postVariables = {
    ...createVariables,
    competition: categoryInfo.selectedComptn?.id || undefined,
    category: props.id
  }

  const { mutate, onDone, error: sendMessageError, onError } = useMutation(gql`    
    
    mutation ($file: Upload, $category: ID, $competition: ID, $description: String!) { 
      createPost (
        file: $file,
        competition: $competition,
        category: $category,
        description: $description
      ) {
          post {
            id
          }  
        }
    }

  `, () => ({
      variables: postVariables
    })
  )

  mutate()

  onDone(() => {
    state.refreshCreatePost++
    state.creatingPost = false
    refetch()
  })

  onError((error: any) => {
    state.creatingPost = false
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else {
      toast.$patch({message: 'Error Occured While Uploading Post', color: 'danger', open: true})
    }
  })
}

function tabChanged(value: string) {
  state.tabSelected = value
  variables.trending.value = value == 'trending'
}

</script>

<style scoped>
ion-breadcrumb {
  font-size: 21px !important;
  font-weight: 500 !important;
  line-height: 1.2;
}
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