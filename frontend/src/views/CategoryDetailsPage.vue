<template>
  <ion-page>
    <ion-content style="height: 100%;" class="ion-padding">

      <ion-grid>

        <ion-row class="ion-justify-content-center">

          <!-- Start of the create post and all posts and breadcrumbs -->
          <ion-col class="posts" size="8" size-xs="12" size-sm="12" size-md="8" size-lg="8" size-xl="8">

            <ion-row>

              <ion-col size="12">

                <ion-breadcrumbs color="primary">
                  <ion-breadcrumb class="cpointer" @click="goBackCategory()">
                    {{ result?.categoryDetails.name }}
                    <ion-icon slot="separator" style="margin-top: 5px" :icon="arrowForward"></ion-icon>
                  </ion-breadcrumb>
                  <ion-breadcrumb v-if="state.competition">{{ state.competition.name }}</ion-breadcrumb>
                  <ion-icon style="margin-top: 7px;" v-if="state.competition" @click="goBackCategory()" class="close-icon ml-auto cpointer" size="large" :icon="closeOutline"></ion-icon>
                </ion-breadcrumbs>

              </ion-col>

              <!-- Competitions for small screens -->
              <ion-col size="12" class="ion-hide-md-up">

                <ion-card class="border-radius-std">

                  <ion-card-header style="padding-bottom: 0px">
                    <ion-card-title>Competitions</ion-card-title>
                  </ion-card-header>

                  <ion-row class="ion-nowrap" style="overflow-y: auto; padding: 5px">
                    <ion-col v-for="(competition, index) in result?.categoryDetails.competitionSet" :key="index">
                      <ion-card @click="loadCompetitionPosts(competition)" class="small-competitions competition cpointer" :class="{'competition-selected': state.competition?.id == competition.id}">
                        <ion-card-header>
                          <ion-card-title>{{ competition.name }}</ion-card-title>
                        </ion-card-header>

                        <ion-card-content>
                          <p class="two-line-ellipsis" :title="competition.description">
                            {{ competition.description }}
                          </p>
                        </ion-card-content>
                      </ion-card>
                    </ion-col>
                  </ion-row>

                </ion-card>

              </ion-col>

              <ion-col size="12" v-if="state.competition">

                <ion-card  class="border-radius-std">
                  <ion-accordion-group>
                    <ion-accordion value="first">
                      <ion-item slot="header" color="light">
                        <ion-label>Competition Details</ion-label>
                      </ion-item>
                      <div class="ion-padding" slot="content">
                        <table style="width:100%">
                          <tr>
                            <td class="header">Description</td>
                            <td>{{ state.competition.description }}</td>
                          </tr>
                          <tr>
                            <td class="header">Last Date</td>
                            <td>{{ state.competition.lastDate }}</td>
                          </tr>
                          <tr>
                            <td class="header">Points</td>
                            <td>{{ state.competition.points }}</td>
                          </tr>
                        </table>
                      </div>
                    </ion-accordion>
                  </ion-accordion-group>
                </ion-card>
                
              </ion-col>

              <ion-col size="12">
                <create-post 
                  :fixed-preview-height="false"
                  :key="state.refreshCreatePost"
                  :competition="state.competition"
                  :creatingPost="state.creatingPost"
                  @uploadPost="createNewPost"
                  type="create"
                >
                </create-post>
              </ion-col>

              <ion-col size="12" v-if="state.competition">
                <!-- <ion-card> -->
                  <ion-segment :value="state.tabSelected" @ionChange="tabChanged">
                    <ion-segment-button value="allposts">
                      <ion-label>All Posts</ion-label>
                    </ion-segment-button>
                    <ion-segment-button value="trending">
                      <ion-label>Top 5</ion-label>
                    </ion-segment-button>
                  </ion-segment>
                <!-- </ion-card> -->
              </ion-col>

              <ion-col size="12" v-for="(post, index) in posts?.allPosts?.posts" :key="post.id">
                <post :post="post"></post>
              </ion-col>

            </ion-row>

          </ion-col>
          <!-- End of the create post and all posts -->

          <!-- Start of competitions for large screens -->
          <ion-col class="ion-hide-md-down" size="4" size-xs="12" size-sm="12" size-md="4" size-lg="4" size-xl="4">

            <ion-card class="border-radius-std">

              <ion-card-header style="padding-bottom: 5px">
                <ion-card-title>Competitions</ion-card-title>
              </ion-card-header>
              
              <ion-row>
                <ion-col size="12" v-for="(competition, index) in result?.categoryDetails.competitionSet" :key="index">
                  <ion-card @click="loadCompetitionPosts(competition)" class="competition cpointer" :class="{'competition-selected': state.competition?.id == competition.id}">
                    <ion-card-header>
                      <ion-card-title>{{ competition.name }}</ion-card-title>
                    </ion-card-header>

                    <ion-card-content>
                      <p class="two-line-ellipsis" :title="competition.description">
                        {{ competition.description }}
                      </p>
                    </ion-card-content>
                  </ion-card>
                </ion-col>
              </ion-row>

            </ion-card>
            
          </ion-col>
          <!-- End of competitions -->

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
import { useQuery } from '@vue/apollo-composable'
import { IonAccordionGroup, IonAccordion, IonItem, IonLabel, IonPage, IonIcon, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonCardTitle, IonBreadcrumb, IonBreadcrumbs, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonSegment, IonSegmentButton, SegmentCustomEvent, SegmentValue } from '@ionic/vue'
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { getPosts } from '@/composables/posts'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'
import { arrowForward, closeOutline } from 'ionicons/icons'

interface CompetitionDetailsType {
  id: number,
  name: string,
  description: string,
  lastDate: string,
  points: number
}

interface State {
  competition: CompetitionDetailsType | null,
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

const props = defineProps({
  id: String
})

const { result, onResult } = useQuery(gql`
                              query ($id: Int!) {
                                categoryDetails (id: $id) {
                                  name,
                                  description,
                                  competitionSet {
                                    id,
                                    name,
                                    description,
                                    lastDate,
                                    points
                                  }
                                }
                              }
                            `, {
                              id: props.id,
                            })

onResult(value => {
  console.log(value)
})

const category =  props.id ? parseInt(props.id) : undefined
const { POST_QUERY, posts, loading, getMore, refetch, variables } = getPosts('allPosts', undefined, category)

function loadCompetitionPosts(competition: CompetitionDetailsType) {
  state.tabSelected = 'allposts'
  state.competition = competition
  variables.competition.value = competition.id
}

function goBackCategory() {
  if (!variables.competition.value) { return }
  variables.competition.value = undefined
  variables.trending.value = false
  state.competition = null
}

function createNewPost(createVariables: updatePostVariables) {

  state.creatingPost = true

  let postVariables = {
    ...createVariables,
    competition: state.competition?.id || undefined,
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
      
      mutation ($file: Upload!, $category: ID, $competition: ID, $description: String!) { 
        createPost (
          file: $file,
          competition: $competition,
          category: $category,
          description: $description
        ) {
            post {
              id, 
              likeCount,
              userLiked,
              description,
              postfileSet {
                file
              },
              user {
                username
              }
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
      variables.page = 1
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
.competition-selected {
  border: 1px solid var(--ion-color-primary)
}
.competition:hover {
  box-shadow: 0 6px 6px -3px rgba(0,0,0,.2),0 10px 14px 1px rgba(0,0,0,.14),0 4px 18px 3px rgba(0,0,0,.12)!important;
  /* border: 1px solid var(--ion-color-primary); */
  /* box-shadow: inset 0 0 0 3px #eee; */
}
ion-breadcrumb {
  font-size: 20px;
}
.posts ion-card {
  margin-left: 0px;
  margin-right: 0px;
}
.small-competitions {
  width: 150px;
  height: 120px;
}
table, th, td {
  border-collapse: collapse;
  padding-bottom: 13px;
  padding-top: 13px;
  color: var(--ion-color-dark);
}
tr {
  border-bottom: 0.5px solid var(--ion-color-medium);
}
tr:last-child {
  border-bottom: 0px;
}
table .header {
  width: 150px;
}
</style>