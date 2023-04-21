<template>
  <ion-app>
    <ion-toast
      position="top"
      :color="store.state.toast.color"
      :is-open="store.state.toast.open"
      :message="store.state.toast.message"
      :duration="5000"
      @didDismiss="store.commit('dismissToast')"
    ></ion-toast>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { apolloClient } from './apollo';
import { provideApolloClient } from "@vue/apollo-composable";
import store from '@/vuex';
import { IonToast } from '@ionic/vue';

provideApolloClient(apolloClient)
</script>
