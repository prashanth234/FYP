<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <p class="page-heading">Explore Your Interests</p>

      <ion-grid class="padding-zero">

        <ion-row class="ion-align-items-center">

          <ion-col class="cat-col ion-align-self-center" size="3" size-xs="12" size-sm="6" size-md="4" size-lg="4" size-xl="3" v-for="(category, index) in result?.categories" :key="index">


            <!-- <ion-card class="cat-card" :class="`${category.type}`" style="position: relative">

              <ion-card-header>
                <ion-card-title class="card-title">
                  {{category.name}}
                </ion-card-title>
              </ion-card-header>

              <img :src="`http://localhost:8000/media/${category.image}`" class="card-image"/>

            </ion-card> -->

            <ion-card class="cpointer cat-card" style="border-radius: 10px;" @click="openCategory(category)">

              <ion-card-content class="cat-card-content">

                <ion-img class="cat-image" :src="`http://localhost:8000/media/${category.image.replace('png', 'jpg')}`">
                </ion-img>

                <div class="cat-title">
                  {{category.name}}
                </div>

                <div class="cat-description">
                  {{category.description}}
                </div>

              </ion-card-content>

            </ion-card>

            <!-- <ion-card class="cpointer cat-card" style="border-radius: 10px;" @click="openCategory(category)">

              <ion-card-content class="cat-card-content">
                
                <ion-img class="cat-image" :src="`http://localhost:8000/media/${category.image}`" style="max-width: 100%;">
                </ion-img>
                
                <div class="cat-title">
                  {{category.name}}
                  <ion-icon class="cat-arrow" :icon="arrowForwardOutline"></ion-icon>
                </div>

              </ion-card-content>

            </ion-card> -->

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
  color: var(--ion-text-color);
  width: fit-content;
  box-shadow: none;
  border: 1px solid #d7d8da;
  margin-left: auto;
  margin-right: auto;
}
.cat-card:hover {
  /* transform: translate3d(0, 5px, 0) rotateX(1deg); */
  border: 2px solid var(--ion-color-primary);
}
.cat-image {
  margin-bottom: 15px;
  height: 220px;
  width: 180px;
  object-fit: cover;
}
.cat-image::part(image) {
  border-radius: 5px;
}
.cat-card-content {
  padding: 25px;
}
.cat-title {
  font-size: 20px;
  font-weight: 500;
}
.cat-description {
  font-size: 13px;
  color: grey
}
.cat-arrow {
  float: right;
  font-size: 25px;
  padding-top: 2px;
  opacity: 0.5;
}
.page-heading {
  margin: 0px;
  font-size: 23px;
  font-weight: 500;
  margin-left: 15px;
}


.card-title {
  font-size: 27px;
  color: white;
  font-weight: 500;
}
.card-image {
  height: 160px;
  width: 110px;
  position: absolute;
  bottom: 0;
  right: 20px;
}
/* .ART {
  background-image: linear-gradient( 135deg,  #0396FF 10%, #ABDCFF 100%);
}
.CAMERA {
  background-image: linear-gradient( 135deg,  #EA5455 10%, #FEB692 100%);
}
.STORY {
  background-image: linear-gradient( 135deg,  #7367F0 10%, #CE9FFC 100%);
}

.POETRY {
  background-image: linear-gradient( 135deg,  #32CCBC 10%, #90F7EC 100%);
} */

.CAMERA .card-image {
  height: 120px;
  width: 130px;
  bottom: 13px;
  right: 18px;
}

.STORY .card-image {
  height: 160px;
  width: 150px;
  bottom: 7px;
  right: 15px;
}

.POETRY .card-image {
  height: 160px;
  width: 150px;
  bottom: 7px;
  right: 15px;
}

.cat-col {
  padding-left: 30px;
  padding-right: 30px;
}


</style>