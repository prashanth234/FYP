<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <h1 style="margin: 0px">Temp</h1>

      {{ ` ${state.name} = ${state.firstname}  ${state.lastname}`}}

      <child v-model="state.name" @update:first-name="firstupdate" v-model:last-name="state.lastname"/>

    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonIcon, IonContent, IonCol, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonCardTitle, IonBreadcrumb, IonBreadcrumbs, IonCard, IonCardHeader, IonCardContent, useIonRouter } from '@ionic/vue'
import { reactive, onMounted, ref } from 'vue'
import Child from './tempComponent.vue'

const state = reactive({
  firstname: '',
  lastname: '',
  name: ''
})

function firstupdate () {
  console.log("parent")
}
</script>

<style scoped>
</style>