<template>
  <ion-page>
    <ion-content style="height: 100%;" class="ion-padding">

      <h1 style="margin: 0px">{{ result?.categoryDetails.name }}</h1>
      
      <ion-card>
        <ion-card-header>
          <ion-card-title>Competitions</ion-card-title>
        </ion-card-header>

        <div>
          <ion-grid>
            <ion-row>
              <ion-col size="3" v-for="(competition, index) in result?.categoryDetails.competitionSet" :key="index">
                <ion-card @click="openCompetition(competition)">
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
        </div>
      </ion-card>

      <ion-card>
          <ion-card-header>
            <ion-card-title>Trending</ion-card-title>
          </ion-card-header>

        <ion-card-content>
          <competition-details-page v-if="competitionId" :id="competitionId"/>
        </ion-card-content>
      </ion-card>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonPage, IonRouterOutlet, IonContent, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonList, IonItem, IonLabel, IonAvatar, IonImg } from '@ionic/vue'
import CompetitionDetailsPage from './CompetitionDetailsPage.vue'

const ionRouter = useIonRouter();

const props = defineProps({
  id: String
})

const { result } = useQuery(gql`
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

watch(result, value => {
      console.log(value)
    })

const competitionId = ref('')   
function openCompetition(competition: Object) {
  competitionId.value = competition.id
  // ionRouter.push(`/category/${props.id}/competition/${competition.id}`)
}

</script>