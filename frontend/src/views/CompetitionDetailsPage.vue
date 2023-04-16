<template>
  
  <div v-if="result?.competitionDetails" class="ion-padding">

    <ion-button @click="setOpen(true)">Participate</ion-button>

    <ion-modal :is-open="isOpen">
      <ion-header>
        <ion-toolbar>
          <ion-title>Create new post</ion-title>
          <ion-buttons slot="end">
            <ion-button @click="setOpen(false)">Close</ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
      <ion-content class="ion-padding">
        <ion-grid>
          <ion-row>
            <ion-col size="12">
              <ion-textarea v-model="description" placeholder="Description" :auto-grow="true" fill="outline"
                value="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris tellus sem, auctor accumsan egestas sed, venenatis at ex. Nam consequat ex odio, suscipit rhoncus orci dictum eget. Aenean sit amet ligula varius felis facilisis lacinia nec volutpat nulla. Duis ullamcorper sit amet turpis sed blandit. Integer pretium massa eu faucibus interdum.">
              </ion-textarea>
            </ion-col>
            <ion-col size="12">
              <input type="file" @change="handleFileUpload" />
              <ion-img style="width: 200px; height: 200px" :src="previewImage" v-if="previewImage"></ion-img>
              <ion-button @click="uploadImage" :disabled="!imageUrl">Upload Image</ion-button>
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-content>
    </ion-modal>

    <ion-grid>
      <ion-row class="ion-justify-content-center" v-for="(post, index) in result.competitionDetails.postSet" :key="index">
        <ion-col size="4">
          <post :post="post"></post>
        </ion-col>
      </ion-row>
    </ion-grid>

  </div>

</template>  

<script setup lang="ts">

import { watch, ref } from 'vue'
import gql from 'graphql-tag'
import { useQuery } from '@vue/apollo-composable'
import { IonTextarea, IonPage, IonContent, IonTitle, IonButton, IonModal, IonHeader, IonToolbar, IonButtons, IonBreadcrumbs, IonCol, IonGrid, IonRow, IonCardTitle, IonCardSubtitle, IonCard, IonCardHeader, IonCardContent, useIonRouter, IonList, IonItem, IonLabel, IonAvatar, IonImg } from '@ionic/vue';
import { useMutation } from '@vue/apollo-composable'

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
                                    id,
                                    name,
                                    description
                                  },
                                  postSet {
                                    id, 
                                    likeCount,
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
const isOpen = ref(false)

function setOpen (value: boolean) {
  isOpen.value = value;
}

const imageUrl = ref('');
const previewImage = ref('');
const description = ref('');

function handleFileUpload({target: { validity, files: [file],},}) {
  if (validity.valid) {
    imageUrl.value = file
    if (file) {
      const reader = new FileReader();

      reader.onload = () => {
        previewImage.value = reader.result;
      };

      reader.readAsDataURL(file);
    }
  }
}

function uploadImage() {
  try {
    const { mutate, onDone } = useMutation(gql`    
      
      mutation ($file: Upload!, $category: ID!, $competition: ID!, $description: String!) { 
        createPost (
          file: $file,
          category: $category,
          competition: $competition,
          description: $description
        ) {
            post {
              category {
                name 
              },
              competition {
                name
              } 
            }  
          } 
      }

    `, {
        // Parameters
        variables: {
          file: imageUrl.value,
          competition: props.id,
          category: result.value.competitionDetails.category.id,
          description: description.value
        }
      }
    )

    mutate()
  } catch (error) {
    console.error(error)
  }
}

</script>