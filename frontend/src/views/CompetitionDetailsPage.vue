<template>
  
  <div v-if="!loading" class="ion-padding">
    
    <create-post :competition="result.competitionDetails">
    </create-post>

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

import { watch, ref } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonCol, IonGrid, IonRow} from '@ionic/vue';
import Post from '@/components/PostContainer.vue'
import CreatePost from '@/components/CreatePostContainer.vue'

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
                            `, {
                              id: props.id,
                            })

watch(result, value => {
      console.log(value)
    })
</script>