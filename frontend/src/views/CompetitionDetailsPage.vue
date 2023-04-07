<template>
  <ion-page>
    <ion-content v-if="result?.competitionDetails" style="height: 100%;" class="ion-padding">
      <ion-breadcrumbs>
        <ion-breadcrumb>{{ result.competitionDetails.category.name }}</ion-breadcrumb>
        <ion-breadcrumb>{{ result.competitionDetails.name }}</ion-breadcrumb>
      </ion-breadcrumbs>
      <h3>{{ result.competitionDetails.description }}</h3>
      <ion-card>
          <ion-card-header>
            <ion-card-title>Posts</ion-card-title>
          </ion-card-header>

        <ion-card-content>
          <ion-grid>
            <ion-row class="ion-justify-content-center">
              <ion-col size="4" v-for="(post, index) in result.competitionDetails.postSet" :key="index">
                <post :post="post"></post>
              </ion-col>
            </ion-row>
          </ion-grid>
        </ion-card-content>
      </ion-card>
    </ion-content>
  </ion-page>

</template>  

<script setup lang="ts">

import { watch } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonPage, IonContent, IonBreadcrumb, IonBreadcrumbs, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonList, IonItem, IonLabel, IonAvatar, IonImg } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'

const ionRouter = useIonRouter();

const props = defineProps({
  id: String
})

const { result } = useQuery(gql`
                              query ($id: Int!) {
                                competitionDetails (id: $id) {
                                  name,
                                  description,
                                  category {
                                    name,
                                    description
                                  },
                                  postSet {
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