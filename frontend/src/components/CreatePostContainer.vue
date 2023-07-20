<template>

    
    <ion-card class="padding-zero margin-zero border-radius-std">

      <ion-header v-if="props.showHeader">
        <ion-toolbar>
          <ion-title>{{ state.title }}</ion-title>
          <ion-buttons slot="end">
            <ion-icon size="large" class="cpointer" :icon="closeOutline" @click="emit('close')"></ion-icon>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>

      <ion-grid>
        <ion-row>

          <ion-col size="12">
            <ion-textarea
              label=""
              v-model="state.description"
              placeholder="Description"
              :auto-grow="true"
            />
          </ion-col>

          <ion-col size="12">
            <div v-if="state.preview" :class="{'preview-image': props.fixedPreviewHeight}" style="margin: 10px">
              <ion-img :src="state.preview"></ion-img>
            </div>
          </ion-col>

          <ion-col size="12">
            <file-upload-container
              v-model:preview="state.preview"
              v-model="state.image"
              :key="state.refreshFileUpload"
              :simple="true"
              :cropable="false"
            >
              <template #handler="{selectImage}">
                <ion-row class="padding-col-zero">
                  <ion-col size="auto">
                    <ion-button
                      @click="selectImage()"
                      for="file-upload"
                      size="small"
                      color="primary"
                    >
                      {{ state.preview ? 'Change Image' : 'Select Image' }}
                    </ion-button>
                  </ion-col>
                  <ion-col>
                    <ion-button
                      size="small"
                      @click="state.uploadAction"
                      :disabled="!state.preview || !!props.creatingPost"
                      style="float: right"
                    >
                      <ion-spinner 
                        class="button-loading-small"
                        v-if="props.creatingPost"
                        name="crescent"
                      />
                      <span v-else>
                        {{ state.uploadTitle }}
                      </span>
                    </ion-button>
                    <ion-button
                      size="small"
                      @click="createPostForm"
                      color="light"
                      class="ion-padding-end"
                      style="float: right"
                    >
                      Clear
                    </ion-button>
                  </ion-col>
                </ion-row>
              </template>  
            </file-upload-container>
          </ion-col>

        </ion-row>
      </ion-grid>
    </ion-card>

</template>

<script lang="ts" setup>
import { IonHeader, IonToolbar, IonTitle, IonButtons, IonIcon, IonTextarea, IonCard, IonSpinner, IonButton, IonCol, IonGrid, IonRow, IonImg } from '@ionic/vue';
import { closeOutline } from 'ionicons/icons'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue'
import store from '@/vuex'
import { updatePostVariables } from '@/mixims/interfaces'
import { useToastStore } from '@/stores/toast'

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
  post?: PostType | null,
  type: string,
  creatingPost?: Boolean,
  showHeader?: Boolean,
  fixedPreviewHeight: Boolean
}>()

const state = reactive({
  image: null,
  preview: '',
  description: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  uploadAction: () => {}
})

const toast = useToastStore()

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'updatePost', variables: updatePostVariables): void;
  (e: 'uploadPost', variables: updatePostVariables): void;
}>()

function createPostForm () {
  state.image = null
  state.description = ''
  state.refreshFileUpload++
}

function uploadPost() {
  const variables: updatePostVariables = {
    file: state.image,
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

  if (state.image && postfileSet[0].file != state.image) {
    Object.assign(variables, { file: state.image })
  }

  if (Object.keys(variables).length == 1) {
    toast.$patch({message: 'No changes made', color: 'warning', open: true})
  } else {
    emit('updatePost', variables)
  }
}

function initialize() {
  if (props.type == 'edit' && props.post) {
    state.title = 'Edit Post'
    state.uploadTitle = 'Update'
    state.description = props.post.description
    state.preview = props.post.postfileSet[0].file
    state.uploadAction = updatePost
  } else if (props.type == 'create') {
    state.title = 'Create Post'
    state.uploadTitle = 'Upload'
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
.preview-image {
  height: 250px;
  overflow: auto;
}
</style>