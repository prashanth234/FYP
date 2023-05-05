<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <h1 style="margin: 0px">Temp</h1>

      <ion-grid>

        <ion-row class="ion-align-items-end">

          <ion-col size="3" size-xs="12" size-sm="6" size-md="4" :size-lg="12/5" :size-xl="12/5" v-for="(category, index) in state.categories" :key="index">

            <ion-card>

              <ion-card-content class="ion-text-center ion-padding">
                <img src="http://localhost:8000/media/categories/ART.jpg" style="max-width: 100%;"/>
              </ion-card-content>

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
  categories: [1,2,3,4,5,6,7,8,9,10,]
})
</script>