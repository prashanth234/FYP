<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <h1 style="margin: 0px">Temp</h1>

      {{ ` ${state.name} = ${state.firstname}  ${state.lastname}`}}


      <ion-col v-for="item in [1,2,3]" :key="item">
        <a @click="routeTo(item)">click item {{item}}</a>
      </ion-col>

      <ion-button @click="router.push('/temp')">back</ion-button>

    </ion-content>

      <ion-router-outlet style="margin-top: 100px;"></ion-router-outlet>
  </ion-page>
</template>

<script lang="ts" setup>
import { IonPage, IonRouterOutlet, IonIcon, IonContent, IonCol, IonButton, IonGrid, IonRow, IonInfiniteScroll, IonInfiniteScrollContent, IonCardTitle, IonBreadcrumb, IonBreadcrumbs, IonCard, IonCardHeader, IonCardContent, useIonRouter } from '@ionic/vue'
import { reactive, onMounted, ref, watch } from 'vue'
import { onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router'
import Child from './tempComponent.vue'

onBeforeRouteUpdate(async (to, from) => {
  // only fetch the user if the id changed as maybe only the query or the hash changed
  // console.log(to, from)
  // console.log("router update in parent")
})

onBeforeRouteLeave(async (to, from) => {
  // only fetch the user if the id changed as maybe only the query or the hash changed
  // console.log(to, from)
  // console.log("router leave in parent")
})

const props = defineProps({
  id: String
})

watch(() => props.id, () => {
  // console.log("id changed", props)
})

const state = reactive({
  firstname: '',
  lastname: '',
  name: ''
})

function firstupdate () {
  console.log("parent")
}

const router = useIonRouter()

function routeTo (item: number) {
  router.push(`/temp/child/${item}`)
}

onMounted(() => {
  // console.log("mounted")
})

</script>

<style scoped>
</style>