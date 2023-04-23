<template>
  
  <div v-if="!loading" class="ion-padding">
    
    <ion-button @click="setOpen(true)" class="ion-text-end">Participate</ion-button>
    <ion-modal :is-open="state.isOpen">
      <create-post :competition="result.competitionDetails" @close="state.isOpen = false" type="create">
      </create-post>
    </ion-modal>

    <ion-grid>
      <ion-row class="ion-justify-content-center" v-for="(post, index) in result.competitionDetails.postSet" :key="index">
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

const props = defineProps({
  id: String
})

const { result, loading } = useQuery(gql`
                              query ($id: Int!) {
                                competitionDetails (id: $id) {
                                  id,
                                  name,
                                  description,
                                  category {
                                    id,
                                    name,
                                    description
                                  },
                                  postSet {
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
                            `, props)

watch(result, value => {
  console.log(value)
})

const state = reactive({
  isOpen: false
})

function setOpen (value: boolean) {
  if (!store.state.user.success) { 
    store.commit('displayAuth')
    return
  }
  state.isOpen = value;
}
</script>