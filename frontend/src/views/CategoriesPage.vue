<template>
  <ion-page>
    <ion-content style="height: 100%;">
      
      <ion-grid>

        <ion-row class="ion-justify-content-center ion-align-items-end">

          <ion-col v-for="(category, index) in result?.categories" :key="index">
            <ion-card @click="openCategory(category)">
              
              <img :alt="category.name" :src="`http://localhost:8000/static/category/${category.type}.png`" height="100" />

              <ion-card-header>
                <ion-card-title>{{category.name}}</ion-card-title>
                <ion-card-subtitle>Card Subtitle</ion-card-subtitle>
              </ion-card-header>

              <ion-card-content>
                {{category.description}}
              </ion-card-content>
            </ion-card>
          </ion-col>
          
        </ion-row>

      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent  } from '@ionic/vue';
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

const { result } = useQuery(gql`
                              query {
                                categories {
                                  name,
                                  description,
                                  type,
                                  id
                                }
                              }
                            `)

function openCategory (category: Object) {
  console.log(category)
}
</script>