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
                <ion-card @click="openCompetition(competition)" class="competition cpointer" :class="{'competition-selected': state.competition == competition.id}">
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
          <!-- <ion-card-header>
            <ion-card-title>Trending</ion-card-title>
          </ion-card-header> -->

        <ion-card-content>
          <competition-details v-if="state.competition" :competition="state.competition"/>
        </ion-card-content>
      </ion-card>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter } from '@ionic/vue'
import CompetitionDetails from '@/components/CompetitionDetailsContainer.vue'

interface CompetitionDetailsType {
  id: string,
  name: string,
  description: string
}

interface State {
  competition: CompetitionDetailsType | null
}

const state:State = reactive({
  competition: null
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

function openCompetition(competition: CompetitionDetailsType) {
  state.competition = competition
}
</script>

<style scoped>
.competition-selected {
  border: 2px solid var(--ion-color-primary)
}
.competition:hover {
  border: 2px solid var(--ion-color-primary);
  box-shadow: inset 0 0 0 3px #eee;
}
.competition {

}
</style>