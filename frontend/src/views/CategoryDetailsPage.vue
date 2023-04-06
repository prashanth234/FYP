<template>
  <ion-page>
    <ion-content style="height: 100%;" class="ion-padding">

      <h1>{{ result?.categoryDetails.name }}</h1>
      
      <ion-card>
          <ion-card-header>
            <ion-card-title>Competitions</ion-card-title>
          </ion-card-header>

        <ion-card-content>
          <ion-grid>
            <ion-row>
              <ion-col size="3" v-for="(competition, index) in result?.categoryDetails.competitionSet" :key="index">
                <ion-card>
                  <ion-card-header>
                    <ion-card-title>{{ competition.name }}</ion-card-title>
                    <ion-card-subtitle>Card Subtitle</ion-card-subtitle>
                  </ion-card-header>

                  <ion-card-content>
                    {{ competition.description }}
                  </ion-card-content>
                </ion-card>
              </ion-col>
            </ion-row>
          </ion-grid>
        </ion-card-content>
      </ion-card>

      <ion-card>
          <ion-card-header>
            <ion-card-title>Trending</ion-card-title>
          </ion-card-header>

        <ion-card-content>
          <ion-grid>
            <ion-row class="ion-justify-content-center">
              <ion-col size="4">
                <post />
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
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonList, IonItem, IonLabel, IonAvatar, IonImg } from '@ionic/vue';
import Post from '@/components/PostContainer.vue'

const props = defineProps({
  id: String
})

const { result } = useQuery(gql`
                              query ($id: Int!) {
                                categoryDetails (id: $id) {
                                  name,
                                  description,
                                  competitionSet {
                                    name,
                                    description
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

<!-- <script>
import gql from 'graphql-tag'

export default {
  apollo: {
      categories: gql`query {
                            categories {
                                name,
                                description,
                                type,
                                id
                            }
                        }`,
  },
  data () {
      return { 
        categories: []
      }
  },
  methods: {
  },
  mounted () {
  }
}
</script> -->