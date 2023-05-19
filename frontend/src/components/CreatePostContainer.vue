<template>

    <!-- <ion-header>
      <ion-toolbar>
        <ion-title>{{ state.title }}</ion-title>
        <ion-buttons slot="end">
          <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="emit('close')"></ion-icon>
        </ion-buttons>
      </ion-toolbar>
    </ion-header> -->
    <!-- <ion-content class="ion-padding"> -->
      <ion-card class="padding-zero border-radius-std">
        <ion-grid>
          <ion-row>
            <ion-col size="12">
              <ion-textarea label="" v-model="state.description" placeholder="Description" :auto-grow="true">
              </ion-textarea>
            </ion-col>
            <ion-col size="12">
              <file-upload-container :key="state.refreshFileUpload" v-model="state.imageUrl" :simple="true">
                <template v-slot:right-slot>
                  <ion-button size="small" @click="state.uploadAction" :disabled="!state.imageUrl || !!props.creatingPost" style="float: right">
                    <ion-spinner class="button-loading-small" v-if="props.creatingPost" name="crescent"></ion-spinner>
                    <span v-else>{{ state.uploadTitle }}</span>
                  </ion-button>
                  <ion-button size="small" @click="createPostForm" color="light" class="ion-padding-end" style="float: right"> Clear </ion-button>
                </template>  
              </file-upload-container>  
            </ion-col>
          </ion-row>
        </ion-grid>
      </ion-card>
    <!-- </ion-content> -->

</template>

<script lang="ts" setup>
import { IonTextarea, IonCard, IonSpinner, IonButton, IonCol, IonGrid, IonRow } from '@ionic/vue';
import { closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue'
import store from '@/vuex'
import { updatePostVariables } from '@/mixims/interfaces'

interface CompetitionDetailsType {
  id: number,
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
  competition?: CompetitionDetailsType | null
  post?: PostType,
  type: string,
  creatingPost?: Boolean
}>()

const state = reactive({
  imageUrl: '',
  description: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  uploadAction: () => {}
})

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'updatePost', variables: updatePostVariables): void;
  (e: 'uploadPost', variables: updatePostVariables): void;
}>()

function createPostForm () {
  state.imageUrl = ''
  state.description = ''
  state.refreshFileUpload++
}

function uploadPost() {
  const variables = {
    file: state.imageUrl,
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