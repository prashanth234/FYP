<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <!-- <h1 style="margin: 0px">Temp</h1>

      {{ ` ${state.name} = ${state.firstname}  ${state.lastname}`}}


      <ion-col v-for="item in [1,2,3]" :key="item">
        <a @click="routeTo(item)">click item {{item}}</a>
      </ion-col>

      <ion-button @click="router.push('/temp')">back</ion-button> -->

      <!-- <div class="grid-container">
          <div class="grid-item" v-for="i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,24,25,26,27,28,29,30]" :key="i">
              <img src="/media/categories/ART.jpg" alt="Image 1">
              <h2>Card {{i}}</h2>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </div>
      </div> -->
      
    </ion-content>

      <!-- <ion-router-outlet style="margin-top: 100px;"></ion-router-outlet> -->
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

body, html {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

/* Create a grid container */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Responsive columns */
    grid-gap: 20px; /* Gap between grid items */
}

/* Style each grid item (card) */
.grid-item {
    border: 1px solid #ccc;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
}

/* Ensure all rows have the same height by using auto for row heights */
.grid-container {
    grid-auto-rows: auto;
}

/* Style the images */
.grid-item img {
    max-width: 100%;
    height: auto;
    object-fit: cover; /* Maintain aspect ratio and cover container */
}

/* Style other elements inside the card */
.grid-item h2 {
    margin: 10px 0;
}

.grid-item p {
    margin: 0;
}
</style>