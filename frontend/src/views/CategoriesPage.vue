<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <p class="page-heading">Explore Your Interests</p>

      <ion-grid>

        <ion-row>

          <ion-col
            size="auto" size-xs="6" size-sm="4" size-md="3" size-lg="3" size-xl="2.4"
            v-for="(category, index) in result?.categories"
            :key="index"
          >

            <ion-card class="cpointer cat-card" @click="openCategory(category)" >

              <ion-card-content class="cat-card-content">

                <ion-img class="cat-image" :src="`/media/${category.image}`">
                </ion-img>

                <div class="cat-title">
                  {{category.name}}
                </div>

                <div class="cat-description" :title="category.description">
                  {{category.description}}
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
import { IonPage, IonContent, IonImg, IonCol, IonGrid, IonRow, IonCard, IonCardContent, useIonRouter  } from '@ionic/vue';
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'

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
                                  id,
                                  image
                                }
                              }
                            `)

onResult(({data, loading}) => {
  // console.log(data, loading)
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
  border: 1px solid var(--ion-color-light-shade);
  margin: auto;
  border-radius: 10px;
}
.cat-card:hover {
  box-shadow: 0 6px 6px -3px rgba(0,0,0,.2),0 10px 14px 1px rgba(0,0,0,.14),0 4px 18px 3px rgba(0,0,0,.12)!important;
}
.cat-image {
  margin-bottom: 10px;
  object-fit: cover;
}
.cat-image::part(image) {
  border-radius: 5px;
}
.cat-card-content {
  padding: 25px;
}
.cat-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--ion-color-dark-tint);
}
@media only screen and (max-width: 992px) {
  .cat-title  {
    font-size: 15px;
  }
  .cat-description {
    font-size: 12px;
  }
}
@media only screen and (max-width: 576px) {
  .cat-card-content {
    padding: 17px;
  }
}
.cat-description {
  font-size: 13px;
  color: grey;
  height: 4.6ch;
  line-height: 2.3ch;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
ion-grid {
  --ion-grid-padding: 5px;
  --ion-grid-column-padding: 10px;
  --ion-grid-column-padding-xs: 8px;
}
</style>