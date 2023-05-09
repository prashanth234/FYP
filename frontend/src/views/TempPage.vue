<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <h1 style="margin: 0px">Temp</h1>

      <ion-grid>

        <ion-row class="ion-align-items-end">

          <ion-col size="3" size-xs="12" size-sm="6" size-md="4" :size-lg="12/5" :size-xl="12/5" v-for="(category, index) in state.categories" :key="index">
            

            <ion-card class="ion-custom-card" style="position: relative">

              <ion-card-header>
                <ion-card-title style="font-size: 30px;font-weight: 500;">Art</ion-card-title>
              </ion-card-header>

              <!-- <ion-card-content class="ion-padding full-height -->
                <img src="http://localhost:8000/media/artwing.png" style="height: 100px; width: 100px; position: absolute; top: 0; left: 50%; transform: translateX(-50%);"/>
              <!-- </ion-card-content> -->

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
.ion-custom-card {
  background-image: linear-gradient( 135deg, #ABDCFF 10%, #0396FF 100%);
  height: 250px;
  --color: var(--ion-color-step-850, #262626)
}
</style>