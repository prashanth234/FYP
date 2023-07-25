<template>

<ion-page>
  <h1>{{user.params.id}}</h1>
    </ion-page>
    
    
    
</template>

<script lang="ts" setup>
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from 'vue-router';
import { IonRouterOutlet, IonPage } from '@ionic/vue';
import { onMounted, watch } from 'vue';

const user = useRoute()

watch(() => user.params.id, () => { 
  // console.log("child watching")
})

onBeforeRouteLeave(() => {
  // console.log('child Router leave', user.params.id)
})

onBeforeRouteUpdate(() => {
  // console.log('child Router update', user.params.id)
})

onMounted(() => {
  // console.log("child mounted")
})

</script>