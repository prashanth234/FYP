<template>
  <ion-card>
    <ion-card-content>
      <ion-list lines="none">
        <ion-item>
          <ion-avatar slot="start">
            <img alt="Silhouette of a person's head" src="https://ionicframework.com/docs/img/demos/avatar.svg" />
          </ion-avatar>
          <ion-label>Prashanth</ion-label>
          <!-- <p>Mar 15th at 3:20 PM</p> -->
        </ion-item>
        <ion-item style="padding-top: 20px; padding-bottom: 20px">
          <ion-img src="https://docs-demo.ionic.io/assets/madison.jpg" alt="The Wisconsin State Capitol building in Madison, WI at night"></ion-img>
        </ion-item>
        <ion-item>
          <p>The Wisconsin State Capitol building in Madison, WI at night</p>
        </ion-item>
        <ion-item>
          <ion-icon :icon="heartOutline" size="large"></ion-icon>
          <ion-label class="ion-padding">200 Likes</ion-label>
        </ion-item>
      </ion-list>
    </ion-card-content>
  </ion-card>
</template>

<script lang="ts" setup>
import { IonList, IonItem, IonImg, IonLabel, IonAvatar, IonCard, IonCardContent, IonButton, IonIcon, useIonRouter  } from '@ionic/vue';
import { heartOutline } from 'ionicons/icons';
</script>