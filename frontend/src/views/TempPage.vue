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

      <ion-button class="add-post" shape="round">
        Add New Post
      </ion-button>

      <br>

      <ion-button class="add-post1" shape="round">
        Add New Post1
      </ion-button>

      <br>

      <ion-button class="add-post2" shape="round">
        Add New Post2
      </ion-button>

      <br>
      
      <ion-button class="add-post3" shape="round">
        Add New Post3
      </ion-button>

      <br>

      <ion-button class="add-post4" shape="round">
        Add New Post4
      </ion-button>

      <br>

      <ion-button class="add-post5" shape="round">
        Add New Post5
      </ion-button>

      <br>
      
      <ion-button class="add-post6" shape="round">
        Add New Post6
      </ion-button>

      <br>

      <ion-button class="add-post7" shape="round">
        Add New Post6
      </ion-button>

      <br>

      <ion-button class="add-post8" shape="round">
        Add New Post6
      </ion-button>

      <br>

      <ion-button class="add-post9" shape="round">
        Add New Post6
      </ion-button>

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
ion-button {
  color: var(--ion-color-light);
  font-size: 16px;
  font-weight: 650;
}
.add-post {
  /* --background: rgb(56,128,255); */
  --background: linear-gradient(90deg, rgba(61,194,255,1) 0%, rgba(56,128,255,1) 100%);
  
}

.add-post1 {
  --background: radial-gradient(circle, rgba(61,194,255,1) 0%, rgba(59,161,255,1) 50%, rgba(56,128,255,1) 100%);
}

.add-post2 {
  --background: linear-gradient(90deg, rgba(49,113,224,1) 0%, rgba(56,128,255,1) 100%);
}

.add-post3 {
  --background: linear-gradient(90deg, rgba(56,128,255,1) 30%, rgba(61,194,255,1) 100%);
}

.add-post4 {
  --background: linear-gradient(90deg, rgba(203,56,255,1) 0%, rgba(61,159,255,1) 100%);
}

.add-post5 {
  --background: linear-gradient(135deg, #0263B7, #1A2B84);
}

.add-post6 {
  /*
* Created with https://www.css-gradient.com
* Gradient link: https://www.css-gradient.com/?c1=54bffc&c2=0d51fc&gt=l&gd=dtl
*/
  --background: linear-gradient(135deg, #54BFFC, #0D51FC);
}

.add-post7 {
  --background: linear-gradient(to right, #1565C0, #b92b27); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

}

.add-post8 {
  --background: linear-gradient(to right, #cc5333, #23074d); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}

.add-post9 {

--background: linear-gradient(to right, #004e92, #000428); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

}

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