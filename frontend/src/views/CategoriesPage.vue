<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <p style="margin: 0px; font-size: 25px; margin-left: 15px;">Explore Your Interests</p>

      <ion-grid class="padding-zero">

        <ion-row class="ion-align-items-end">

          <ion-col class="padding-zero" size="3" size-xs="12" size-sm="6" size-md="4" :size-lg="3" :size-xl="3" v-for="(category, index) in result?.categories" :key="index">

            <ion-card class="cpointer cat-card" style="border-radius: 10px;" @click="openCategory(category)">

              <ion-card-content class="cat-card-content">
                
                <ion-img class="cat-image" :src="`http://localhost:8000/media/${category.image}`" style="max-width: 100%;">
                </ion-img>
                
                <div class="cat-title">
                  {{category.name}}
                  <ion-icon class="cat-arrow" :icon="arrowForwardOutline"></ion-icon>
                </div>

              </ion-card-content>

            </ion-card>

          </ion-col>
          
        </ion-row>

      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonImg, IonIcon, IonModal, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter  } from '@ionic/vue';
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { arrowForwardOutline } from 'ionicons/icons'

const ionRouter = useIonRouter();

interface categoryObject {
  name: string,
  description: string,
  type: string,
  id: number,
  image: string
}

const { result, onResult } = useQuery(gql`
                              query {
                                categories {
                                  name,
                                  description,
                                  type,
                                  id,
                                  image
                                }
                              }
                            `)

onResult(({data, loading}) => {
  console.log(data, loading)
})

function openCategory (category: categoryObject) {
  ionRouter.push(`category/${category.id}`)
}
</script>

<style scoped>
.cat-card {
  color: var(--color);
}
.cat-card:hover {
  transform: translate3d(0, 10px, 0) rotateX(10deg);
}
.cat-image {
  padding-bottom: 10px;
}
.cat-image::part(image) {
  border-radius: 5px;
}
.cat-card-content {
  padding: 10px;
}
.cat-title {
  font-size: 16px;
  font-weight: 500;
}
.cat-arrow {
  float: right;
  font-size: 25px;
  padding-top: 2px;
  opacity: 0.5;
}
</style>