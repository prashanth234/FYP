<template>
  <ion-app>
    <toast />
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { apolloClient } from './apollo';
import { provideApolloClient } from "@vue/apollo-composable";
import Toast from './components/ToastContainer.vue';

provideApolloClient(apolloClient)
</script>
