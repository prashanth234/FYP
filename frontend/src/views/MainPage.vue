<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>TBD</ion-title>
        <ion-icon :icon="logOutOutline" size="large"></ion-icon>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-router-outlet></ion-router-outlet>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon } from '@ionic/vue';
import { logOutOutline } from 'ionicons/icons';
</script>