<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <p class="page-heading">Explore Your Interests</p>

      <ion-grid>

        <ion-row>

          <ion-col
            size="auto" size-xs="6" size-sm="4" size-md="3" size-lg="3" size-xl="2.4"
            v-for="(cat, index) in category.categories"
            :key="index"
          >

            <ion-card class="cpointer cat-card" @click="openCategory(cat)" >

              <ion-card-content class="cat-card-content">

                <ion-img class="cat-image" :src="`/media/${cat.image}`">
                </ion-img>

                <div class="cat-title">
                  {{cat.name}}
                </div>

                <div class="cat-description" :title="cat.description">
                  {{cat.description}}
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
import { useCategoryStore } from '@/stores/category';
import { IonPage, IonContent, IonImg, IonCol, IonGrid, IonRow, IonCard, IonCardContent, useIonRouter  } from '@ionic/vue';
import { categoryObject } from '@/mixims/interfaces'

const ionRouter = useIonRouter();
const category = useCategoryStore();

category.getCategories()

function openCategory (category: categoryObject) {
  ionRouter.push(`interests/${category.id}`)
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
  /* box-shadow: 0 3px 3px -3px rgba(0,0,0,.2),0 5px 7px 1px rgba(0,0,0,0),0 2px 9px 1px rgba(0,0,0,.2)!important; */
  box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
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
ion-grid {
  --ion-grid-padding: 5px;
  --ion-grid-padding-xs: 0px;
  --ion-grid-column-padding: 10px;
  --ion-grid-column-padding-xs: 8px;
}
</style>