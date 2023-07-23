<template>
  <ion-page>
    <ion-content style="height: 100%;" class="ion-padding">

      <ion-grid>

        <ion-row class="ion-justify-content-center">

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row>

              <!-- Breadcrumb for navigation from category to competition -->
              <ion-col size="12">

                <ion-breadcrumbs color="primary">
                  <ion-breadcrumb class="cpointer" @click="goBackCategory()">
                    {{ categoryInfo.name }}
                    <ion-icon slot="separator" style="margin-top: 5px" :icon="arrowForward"></ion-icon>
                  </ion-breadcrumb>
                  <ion-breadcrumb v-if="categoryInfo.selectedComptn">{{ categoryInfo.selectedComptn.name }}</ion-breadcrumb>
                  <ion-icon style="margin-top: 7px;" v-if="categoryInfo.selectedComptn" @click="goBackCategory()" class="close-icon ml-auto cpointer" size="large" :icon="closeOutline"></ion-icon>
                </ion-breadcrumbs>

              </ion-col>

              <!-- Competitions for small screens -->
              <ion-col size="12" class="ion-hide-md-up">
                <competitions
                  @select-competition="loadCompetitionPosts"
                  :vertical="false"
                />
              </ion-col>

              <!-- Competition details -->
              <ion-col size="12" v-if="categoryInfo.selectedComptn">
                <competition-details />
              </ion-col>

              <!-- Create Post -->
              <ion-col size="12" v-if="!categoryInfo.loading">
                <create-post
                  :fixed-preview-height="false"
                  :key="state.refreshCreatePost"
                  :creatingPost="state.creatingPost"
                  @uploadPost="createNewPost"
                  type="create"
                >
                </create-post>
              </ion-col>

              <!-- Toggle between all posts and top 5 -->
              <ion-col size="12" v-if="categoryInfo.selectedComptn">
                <ion-segment :value="state.tabSelected" @ionChange="tabChanged">
                  <ion-segment-button value="allposts">
                    <ion-label>All Posts</ion-label>
                  </ion-segment-button>
                  <ion-segment-button value="trending">
                    <ion-label>Top 5</ion-label>
                  </ion-segment-button>
                </ion-segment>
              </ion-col>

              <!-- Display the posts -->
              <ion-col size="12" v-for="(post, index) in posts?.allPosts?.posts" :key="post.id">
                <post :post="post"></post>
              </ion-col>

            </ion-row>

          </ion-col>

          <!-- Competitions for large screens -->
          <ion-col class="ion-hide-md-down" size="4" size-xs="12" size-sm="12" size-md="4" size-lg="4" size-xl="4">
            <competitions
              @select-competition="loadCompetitionPosts"
              :vertical="true"
            />
          </ion-col>

        </ion-row>

      </ion-grid>

      <ion-infinite-scroll @ionInfinite="getMore">
        <ion-infinite-scroll-content></ion-infinite-scroll-content>
      </ion-infinite-scroll>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import gql from 'graphql-tag'
import { IonLabel, IonPage, IonIcon, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonBreadcrumb, IonBreadcrumbs, useIonRouter, IonSegment, IonSegmentButton, SegmentCustomEvent, SegmentValue } from '@ionic/vue'
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { getPosts } from '@/composables/posts'
import { UpdatePostVariables, CompetitionInfo } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'
import { arrowForward, closeOutline } from 'ionicons/icons'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import Competitions from '@/components/CompetitionsContainer.vue'
import CompetitionDetails from '@/components/CompetitionInfoContainer.vue'

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

const ionRouter = useIonRouter();
const categoryInfo = useCategoryInfoStore();

const props = defineProps({
  id: String
})

if (props.id) {
  categoryInfo.getCategoryInfo(props.id)
}

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

  state.creatingPost = true

  let postVariables = {
    ...createVariables,
    competition: categoryInfo.selectedComptn?.id || undefined,
    category: props.id
  }

  // const CACHE_VARIABLES = {
  //   page: 1,
  //   perPage: variables.perPage,
  //   competition: variables.competition.value,
  //   category: variables.category.value
  // }

  try {
    const { mutate, onDone } = useMutation(gql`    
      
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
        variables: postVariables,
        // Here posts will be overriden when more posts are fetched in the posts composable (need to think, how to show new posts) 
        // update: (cache, { data: { createPost } }) => {
        //   let data = cache.readQuery<QueryResult>({ query: POST_QUERY, variables: CACHE_VARIABLES })
        //   if (!data) { return }
        //   data = {
        //     ...data,
        //     allPosts: {
        //       ...data.allPosts,
        //       posts: [
        //         createPost.post,
        //         ...data.allPosts.posts,
        //       ]
        //     }
        //   }
        //   cache.writeQuery({ query: POST_QUERY, variables: CACHE_VARIABLES, data })
        // },
      })
    )

    mutate()

    onDone(() => {
      state.refreshCreatePost++
      state.creatingPost = false
      refetch()
    })

  } catch (error) {
    console.error(error)
  }
}

function tabChanged(event: SegmentCustomEvent) {
  state.tabSelected = event.target.value
  variables.trending.value = event.target.value == 'trending'
}

</script>

<style scoped>
ion-breadcrumb {
  font-size: 20px;
}
.posts ion-card {
  margin-left: 0px;
  margin-right: 0px;
}
</style>