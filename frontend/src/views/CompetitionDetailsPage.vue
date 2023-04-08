<template>
  <ion-page>

    <ion-content v-if="result?.competitionDetails" style="height: 100%;" class="ion-padding">

      <ion-title>Category: {{ result.competitionDetails.category.name }}</ion-title>
      <ion-title>Competition: {{ result.competitionDetails.name }}</ion-title>
      <ion-title>Description: {{ result.competitionDetails.description }}</ion-title>

      <ion-button id="open-modal" expand="block">Participate</ion-button>
      <p>{{ message }}</p>
      <ion-modal ref="modal" trigger="open-modal" @willDismiss="onWillDismiss">
        <ion-header>
          <ion-toolbar>
            <ion-buttons slot="start">
              <ion-button @click="cancel()">Cancel</ion-button>
            </ion-buttons>
            <ion-title>Welcome</ion-title>
            <ion-buttons slot="end">
              <ion-button :strong="true" @click="confirm()">Confirm</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding">
          <ion-item>
            <ion-label position="stacked">Enter your name</ion-label>
            <ion-input ref="input" type="text" placeholder="Your name"></ion-input>
          </ion-item>
        </ion-content>
      </ion-modal>

      <ion-card>

        <ion-card-header>
          <ion-card-title>Posts</ion-card-title>
        </ion-card-header>

        <ion-card-content>
          <ion-grid>
            <ion-row class="ion-justify-content-center" v-for="(post, index) in result.competitionDetails.postSet" :key="index">
              <ion-col size="4">
                <post :post="post"></post>
              </ion-col>
            </ion-row>
          </ion-grid>
        </ion-card-content>

      </ion-card>
    </ion-content>

  </ion-page>

</template>  

<script setup lang="ts">

import { watch, ref } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonPage, IonContent, IonTitle, IonBreadcrumbs, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonList, IonItem, IonLabel, IonAvatar, IonImg } from '@ionic/vue';
import { OverlayEventDetail } from '@ionic/core/components'

import Post from '@/components/PostContainer.vue'

const ionRouter = useIonRouter();

const props = defineProps({
  id: String
})

const { result } = useQuery(gql`
                              query ($id: Int!) {
                                competitionDetails (id: $id) {
                                  name,
                                  description,
                                  category {
                                    name,
                                    description
                                  },
                                  postSet {
                                    description,
                                    postfileSet {
                                      file
                                    },
                                    user {
                                      username
                                    }
                                  }
                                }
                              }
                            `, {
                              id: props.id,
                            })

watch(result, value => {
      console.log(value)
    })

const message = ref('This modal example uses triggers to automatically open a modal when the button is clicked.')
const modal = ref(null)

function cancel () {
  // modal.value.dismiss(null, 'cancel');
  console.log(modal.value)
}

function confirm() {
  const name = modal.$el.value;
  modal.value.dismiss(name, 'confirm');
}

function onWillDismiss(ev: CustomEvent<OverlayEventDetail>) {
  if (ev.detail.role === 'confirm') {
    message.value = `Hello, ${ev.detail.data}!`;
  }
}

</script>