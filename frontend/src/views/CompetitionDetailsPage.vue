<template>
  
  <div v-if="result?.competitionDetails" class="ion-padding">

    <ion-button @click="setOpen(true)">Participate</ion-button>

    <ion-modal :is-open="isOpen">
      <ion-header>
        <ion-toolbar>
          <ion-title>Create New Post</ion-title>
          <ion-buttons slot="end">
            <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="setOpen(false)"></ion-icon>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
      <ion-content class="ion-padding">
        <ion-grid>
          <ion-row>
            <ion-col size="12">
              <ion-textarea class="textarea" v-model="description" placeholder="Description" :auto-grow="true">
              </ion-textarea>
            </ion-col>
            <ion-col size="12">
              <file-upload-container v-model="imageUrl" />
            </ion-col>
            <ion-col style="text-align: center;">
              <ion-button @click="uploadImage" :disabled="!imageUrl">Upload Post</ion-button>
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
import { IonTextarea, IonIcon, IonContent, IonTitle, IonButton, IonModal, IonHeader, IonToolbar, IonButtons, IonCol, IonGrid, IonRow} from '@ionic/vue';
import { useMutation } from '@vue/apollo-composable'
import { closeOutline } from 'ionicons/icons'
import Post from '@/components/PostContainer.vue'
import FileUploadContainer from '@/components/FileUploadContainer.vue'

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

const isOpen = ref(false)
const imageUrl = ref('')
const description = ref('')

function setOpen (value: boolean) {
  isOpen.value = value;
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

<style>
.textarea {
  border: 1px solid #dddfe2;
  padding: 20px;
  border-radius: 4px;
}
</style>