<template>
  
  <div class="ion-padding">
    
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

const { posts, loading, getMore } = getPosts('allPosts')

function setOpen(value: boolean) {
  if (!store.state.user.success) { 
    store.commit('displayAuth')
    return
  }
  state.isOpen = value;
}
</script>