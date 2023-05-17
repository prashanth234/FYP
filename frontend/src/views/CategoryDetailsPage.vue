<template>
  <ion-page>
    <ion-content style="height: 100%;" class="ion-padding">

      <h1 class="page-heading">{{ result?.categoryDetails.name }}</h1>

      <ion-grid>
        <ion-row>

          <!-- Start of the create post and all posts -->
          <ion-col size="8">

            <ion-row class="ion-justify-content-center">

              <ion-col size="11">
                <create-post  
                  :key="state.refreshCreatePost"
                  :competition="state.competition"
                  :creatingPost="state.creatingPost"
                  @uploadPost="createNewPost"
                  type="create"
                >
                </create-post>
              </ion-col>

              <ion-col size="11" v-for="(post, index) in posts?.allPosts?.posts" :key="post.id">
                <post :post="post"></post>
              </ion-col>

            </ion-row>

          </ion-col>
          <!-- End of the create post and all posts -->
          
          <!-- Start of competitions -->
          <ion-col size="4">

            <ion-card class="border-radius-std">

              <ion-card-header>
                <ion-card-title>Competitions</ion-card-title>
              </ion-card-header>

              <ion-row>
                <ion-col size="12" v-for="(competition, index) in result?.categoryDetails.competitionSet" :key="index">
                  <ion-card @click="loadCompetitionPosts(competition)" class="competition cpointer" :class="{'competition-selected': state.competition?.id == competition.id}">
                    <ion-card-header>
                      <ion-card-title>{{ competition.name }}</ion-card-title>
                    </ion-card-header>

                    <ion-card-content>
                      {{ competition.description }}
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
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter } from '@ionic/vue'
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import { getPosts } from '@/composables/posts'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'

interface CompetitionDetailsType {
  id: number,
  name: string,
  description: string
}

interface State {
  competition: CompetitionDetailsType | null,
  refreshCreatePost: number,
  creatingPost: Boolean
}

const state: State = reactive({
  competition: null,
  creatingPost: false,
  refreshCreatePost: 1
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
                                    description
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
const { POST_QUERY, posts, loading, getMore, variables } = getPosts('allPosts', undefined, category)

function loadCompetitionPosts(competition: CompetitionDetailsType) {
  state.competition = competition
  variables.page = 1
  variables.competition.value = competition.id
}

function createNewPost(createVariables: updatePostVariables) {

  state.creatingPost = true

  let postVariables = {
    ...createVariables,
    competition: state.competition?.id || undefined,
    category: props.id
  }

  const CACHE_VARIABLES = {
    page: 1,
    perPage: variables.perPage,
    // competition: variables.competition.value,
    category: variables.category.value
  }

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
        update: (cache, { data: { createPost } }) => {
          let data = cache.readQuery<QueryResult>({ query: POST_QUERY, variables: CACHE_VARIABLES })
          console.log(data, CACHE_VARIABLES)
          if (!data) { return }
          data = {
            ...data,
            allPosts: {
              ...data.allPosts,
              posts: [
                createPost.post,
                ...data.allPosts.posts,
              ]
            }
          }
          console.log(data)
          cache.writeQuery({ query: POST_QUERY, data })
        },
      })
    )

    mutate()

    onDone(() => {
      state.refreshCreatePost++
      state.creatingPost = false
    })

  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.competition-selected {
  border: 2px solid var(--ion-color-primary)
}
.competition:hover {
  border: 2px solid var(--ion-color-primary);
  box-shadow: inset 0 0 0 3px #eee;
}
</style>