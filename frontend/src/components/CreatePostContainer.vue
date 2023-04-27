<template>
  
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ state.title }}</ion-title>
        <ion-buttons slot="end">
          <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="emit('close')"></ion-icon>
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
            <ion-button @click="state.uploadAction" :disabled="!state.imageUrl">{{ state.uploadTitle }}</ion-button>
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-content>

</template>

<script lang="ts" setup>
import { IonTextarea, IonIcon, IonContent, IonTitle, IonButton, IonHeader, IonToolbar, IonButtons, IonCol, IonGrid, IonRow } from '@ionic/vue';
import { closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue'
import store from '@/vuex'
import { updatePostVariables } from '@/mixims/interfaces'

interface CompetitionDetailsType {
  id: string,
  name: string,
  description: string
}

interface PostFileType {
  file: string
}

interface PostType {
  id: number,
  description: string,
  postfileSet: PostFileType[]
}

const props = defineProps<{
  competition?: CompetitionDetailsType
  post?: PostType,
  type: string
}>()

const state = reactive({
  imageUrl: '',
  description: '',
  title: '',
  uploadTitle: '',
  uploadAction: () => {}
})

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'updatePost', variables: updatePostVariables): void;
  (e: 'uploadPost', variables: updatePostVariables): void;
}>()

function uploadPost() {
  if (!props.competition) { return }

  const variables = {
    file: state.imageUrl,
    competition: props.competition.id,
    description: state.description
  }

  emit('uploadPost', variables)
}

function updatePost() {
  if (!props.post) { return }
  const variables = { id: props.post.id }
  const {description, postfileSet} = props.post

  if (description != state.description) {
    Object.assign(variables, { description: state.description })
  }

  if (postfileSet[0].file != state.imageUrl) {
    Object.assign(variables, { file: state.imageUrl })
  }

  if (Object.keys(variables).length == 1) {
    store.commit('displayToast', {message: 'No changes made', color: 'warning'})
  } else {
    emit('updatePost', variables)
  }
}

function initialize() {
  if (props.type == 'edit' && props.post) {
    state.title = 'Edit Post'
    state.uploadTitle = 'Update Post'
    state.description = props.post.description
    state.imageUrl = props.post.postfileSet[0].file
    state.uploadAction = updatePost
  } else if (props.type == 'create') {
    state.title = 'Create Post'
    state.uploadTitle = 'Upload Post'
    state.uploadAction = uploadPost
  }
}

initialize()
</script>

<style scoped>
.textarea {
  border: 1px solid #dddfe2;
  padding: 20px;
  border-radius: 4px;
}
</style>