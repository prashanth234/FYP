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
                <create-post :competition="state.competition" @uploadPost="createNewPost" @close="state.isOpen = false" type="create">
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
import store from '@/vuex'
import { getPosts } from '@/composables/posts'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'

interface CompetitionDetailsType {
  id: number,
  name: string,
  description: string
}

interface State {
  competition: CompetitionDetailsType | null
  isOpen: Boolean
}

const state:State = reactive({
  competition: null,
  isOpen: false
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

let { POST_QUERY, posts, loading, getMore, variables } = getPosts('allPosts')

function loadCompetitionPosts(competition: CompetitionDetailsType) {
  state.competition = competition

  const { POST_QUERY: PQ, posts: pts, loading, getMore: more, variables: vars } = getPosts('allPosts', competition.id)

  POST_QUERY = PQ
  posts = pts
  getMore = more
  variables = vars
}

function createNewPost(createVariables: updatePostVariables) {
  try {
    const { mutate, onDone } = useMutation(gql`    
      
      mutation ($file: Upload!, $competition: ID!, $description: String!) { 
        createPost (
          file: $file,
          competition: $competition,
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
        variables: createVariables,
        // Here posts will be overriden when more posts are fetched in the posts composable (need to think, how to show new posts) 
        update: (cache, { data: { createPost } }) => {
          let data = cache.readQuery<QueryResult>({ query: POST_QUERY, variables })
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
          cache.writeQuery({ query: POST_QUERY, data })
        },
      })
    )

    mutate()
    state.isOpen = false
  } catch (error) {
    console.error(error)
  }
}

// function setOpen(value: boolean) {
//   if (!store.state.user.success) { 
//     store.commit('displayAuth')
//     return
//   }
//   state.isOpen = value;
// }
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