<template>
  
  <div class="ion-padding">

    <ion-button @click="getMore" class="ion-text-end">Fetch More</ion-button>
    
    <ion-button @click="setOpen(true)" class="ion-text-end">Participate</ion-button>
    <ion-modal :is-open="state.isOpen">
      <create-post :competition="props.competition" @close="state.isOpen = false" type="create">
      </create-post>
    </ion-modal>

    <ion-grid>
      <ion-row class="ion-justify-content-center" v-for="(post, index) in posts?.allPosts?.posts" :key="index">
        <ion-col size="4">
          <post :post="post"></post>
        </ion-col>
      </ion-row>
    </ion-grid>

  </div>

</template>  

<script setup lang="ts">

import { watch, reactive } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonCol, IonGrid, IonRow, IonButton, IonModal } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'
import store from '@/vuex'

interface CompetitionDetails {
  id: string,
  name: string,
  description: string
}

const props = defineProps<{
  competition: CompetitionDetails
}>()

const state = reactive({
  isOpen: false,
  page: 1
})

const { result: posts, loading, fetchMore } = useQuery(gql`
                              query ($category: Int, $competition: Int, $page: Int!, $perPage: Int!) {
                                allPosts (category: $category, competition: $competition, page: $page, perPage: $perPage) {
                                  posts {
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
                                  },
                                  total
                                }
                              }
                            `, () => ({
                              page: 1,
                              perPage: 1
                            }))

watch(posts, value => {
  console.log(value)
})

function getMore() {
  if (state.page == posts.value.allPosts.total) { return }

  state.page++

  fetchMore({
    variables: {
      page: state.page
    },
    updateQuery: (previousResult, { fetchMoreResult }) => {
      // No new feed posts
      if (!fetchMoreResult) return previousResult

      // Concat previous feed with new feed posts
      return {
        ...previousResult,
        allPosts: {
          ...previousResult.allPosts,
          posts: [
            ...previousResult.allPosts.posts,
            ...fetchMoreResult.allPosts.posts
          ]
        }
      }
    },
  })
 }

function setOpen(value: boolean) {
  if (!store.state.user.success) { 
    store.commit('displayAuth')
    return
  }
  state.isOpen = value;
}
</script>