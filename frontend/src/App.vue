<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { apolloClient } from './apollo';
import { provideApolloClient } from "@vue/apollo-composable";

provideApolloClient(apolloClient)
</script>
