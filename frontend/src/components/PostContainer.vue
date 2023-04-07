<template>
  <ion-card>
    <ion-card-content>
      <ion-list lines="none">
        <ion-item>
          <ion-avatar slot="start">
            <img alt="Silhouette of a person's head" src="https://ionicframework.com/docs/img/demos/avatar.svg" />
          </ion-avatar>
          <ion-label>{{post.user.username}}</ion-label>
          <!-- <p>Mar 15th at 3:20 PM</p> -->
        </ion-item>
        <ion-item style="padding-top: 20px; padding-bottom: 20px">
          <ion-img :src="`http://localhost:8000/${[post.postfileSet[0].file]}`" alt="The Wisconsin State Capitol building in Madison, WI at night"></ion-img>
        </ion-item>
        <ion-item>
          <p>{{post.description}}</p>
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

defineProps(['post'])

</script>