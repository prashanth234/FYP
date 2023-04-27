<template>
  
  <div class="ion-padding">
    
    <ion-button @click="setOpen(true)" class="ion-text-end">Participate</ion-button>
    <ion-modal :is-open="state.isOpen">
      <create-post :competition="props.competition" @uploadPost="createNewPost" @close="state.isOpen = false" type="create">
      </create-post>
    </ion-modal>

    <ion-grid>
      <ion-row class="ion-justify-content-center" v-for="(post, index) in posts?.allPosts?.posts" :key="index">
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
import { updatePostVariables } from '@/mixims/interfaces'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

interface CompetitionDetails {
  id: string,
  name: string,
  description: string
}

const props = defineProps<{
  competition: CompetitionDetails
}>()

const state = reactive({
  isOpen: false
})

const { POST_QUERY, posts, loading, getMore } = getPosts('allPosts')

console.log(POST_QUERY)

function createNewPost(variables: updatePostVariables) {
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
        variables,
        update: (cache, { data: { createPost } }) => {
          let data = cache.readQuery({ query: POST_QUERY })
          console.log(data)
          data.allPosts.posts = [createPost.post, ...data.allPosts.posts]
          cache.writeQuery({ query: POST_QUERY, data })
        },
      })
    )

    mutate()
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