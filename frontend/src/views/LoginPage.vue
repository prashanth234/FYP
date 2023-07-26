<template>
  <ion-page>
    <ion-content class="ion-text-center full-height">

      <ion-grid class="full-height">
        <ion-row class="ion-justify-content-center ion-align-items-center full-height">

          <ion-col size="6">
            <login-container />
          </ion-col>

        </ion-row>
      </ion-grid>
      
    </ion-content>
  </ion-page>
</template>

<script lang="ts" setup>

import { IonPage, IonContent, IonCol, IonGrid, IonRow } from '@ionic/vue';
import LoginContainer from '@/components/LoginContainer.vue'

</script>