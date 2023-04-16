<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-grid>
          <ion-row class="ion-align-items-center">
            <ion-col>
              <ion-title>TBD</ion-title>
            </ion-col>
            <ion-col size="auto">
              <ion-icon class="icon-custom" :icon="logOutOutline" @click="logout()"></ion-icon>
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-router-outlet></ion-router-outlet>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonRouterOutlet, IonContent, IonHeader, IonToolbar, IonTitle, IonIcon, IonGrid, IonCol, IonRow, useIonRouter } from '@ionic/vue';
import { logOutOutline } from 'ionicons/icons';
import store from '@/vuex';

const ionRouter = useIonRouter();

function logout() {
  localStorage.removeItem('fyptoken')
  localStorage.removeItem('fyprefreshtoken')
  store.commit('storeUser', {})
  ionRouter.push('/login')
}
</script>

<style scoped>
  .icon-custom {
    padding-right: 15px;
  }
  ion-grid {
    --ion-grid-padding: 0px;
    padding-top: 5px;
    font-size: 25px !important
  }
</style>