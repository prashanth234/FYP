<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <h1 style="margin: 0px">Temp</h1>

      <ion-grid>

        <ion-row class="ion-align-items-end">

          <ion-col size="3" size-xs="12" size-sm="6" size-md="4" :size-lg="12/5" :size-xl="12/5" v-for="(category, index) in state.categories" :key="index">
            

            <ion-card class="card" :class="'art'" style="position: relative">

              <ion-card-header>
                <ion-card-title style="font-size: 30px; color: white; font-weight: 500;">Art</ion-card-title>
              </ion-card-header>

              <img src="http://localhost:8000/media/pens.png" style="height: 160px; width: 110px; position: absolute; bottom: 0; right: 20px;"/>

            </ion-card>

          </ion-col>
          
        </ion-row>

      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import {reactive} from 'vue'

const state = reactive({
  categories: [1]
})
</script>

<style scoped>
.art {
  background-image: linear-gradient( 135deg,  #0396FF 10%, #ABDCFF 100%);
}
.photography {
  background-image: linear-gradient( 135deg,  #EA5455 10%, #FEB692 100%);
}
.card {
  height: 250px;
}
</style>