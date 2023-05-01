<template>
  
  <div class="ion-padding">
    
    <ion-button @click="setOpen(true)" class="ion-text-end">Participate</ion-button>
    <ion-modal :is-open="state.isOpen">
      <create-post :competition="props.competition" @uploadPost="createNewPost" @close="state.isOpen = false" type="create">
      </create-post>
    </ion-modal>

    <ion-grid>
      <ion-row class="ion-justify-content-center" v-for="(post, index) in posts?.allPosts?.posts" :key="post.id">
        <ion-col size="4">
          <post :post="post"></post>
        </ion-col>
      </ion-row>
    </ion-grid>

    <ion-infinite-scroll @ionInfinite="getMore">
      <ion-infinite-scroll-content></ion-infinite-scroll-content>
    </ion-infinite-scroll>

  </div>

</template>  

<script setup lang="ts">

import { reactive } from 'vue'
import { IonCol, IonGrid, IonRow, IonButton, IonModal, IonInfiniteScroll, IonInfiniteScrollContent } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import store from '@/vuex'
import { getPosts } from '@/composables/posts'
import { updatePostVariables, Post as PostType } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

interface CompetitionDetails {
  id: string,
  name: string,
  description: string
}

interface QueryResult {
  allPosts: {
    posts: PostType[],
    total: number
  }
}

const props = defineProps<{
  competition: CompetitionDetails
}>()

const state = reactive({
  isOpen: false
})

const { POST_QUERY, posts, loading, getMore, variables } = getPosts('allPosts')

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

function setOpen(value: boolean) {
  if (!store.state.user.success) { 
    store.commit('displayAuth')
    return
  }
  state.isOpen = value;
}
</script>