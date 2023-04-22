<template>
  <ion-button @click="setOpen(true)" class="ion-text-end">Participate</ion-button>
  <ion-modal :is-open="state.isOpen">
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
            <ion-textarea class="textarea" v-model="state.description" placeholder="Description" :auto-grow="true">
            </ion-textarea>
          </ion-col>
          <ion-col size="12">
            <file-upload-container v-model="state.imageUrl" />
          </ion-col>
          <ion-col style="text-align: center;">
            <ion-button @click="uploadImage" :disabled="!state.imageUrl">Upload Post</ion-button>
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-content>
  </ion-modal>
</template>

<script lang="ts" setup>
import gql from 'graphql-tag'
import { IonTextarea, IonModal, IonIcon, IonContent, IonTitle, IonButton, IonHeader, IonToolbar, IonButtons, IonCol, IonGrid, IonRow} from '@ionic/vue';
import { useMutation } from '@vue/apollo-composable'
import { closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue'
import store from '@/vuex'

interface CompetitionType {
  id: number,
  category: {
    id: number
  }
}

const props = defineProps<{
  competition: CompetitionType
}>()

const state = reactive({
  imageUrl: '',
  description: '',
  isOpen: false
})

function uploadImage() {
  try {
    const { mutate, onDone } = useMutation(gql`    
      
      mutation ($file: Upload!, $competition: ID!, $description: String!) { 
        createPost (
          file: $file,
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
          file: state.imageUrl,
          competition: props.competition.id,
          description: state.description
        }
      }
    )

    mutate()
  } catch (error) {
    console.error(error)
  }
}

function setOpen (value: boolean) {
  if (!store.state.user.success) { 
    store.commit('displayAuth')
    return
  }
  state.isOpen = value;
}
</script>

<style>
.textarea {
  border: 1px solid #dddfe2;
  padding: 20px;
  border-radius: 4px;
}
</style>