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

          <ion-col size="12" v-if="state.oftype == 'IMAGETEXT' && state.preview">
            <div :class="{'preview-image': props.fixedPreviewHeight}" style="margin: 10px">
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
                  <ion-col size="auto" v-if="state.oftype == 'IMAGETEXT'">
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
                      :disabled="(state.oftype == 'IMAGETEXT' && !state.preview) || !!state.creatingPost"
                      style="float: right"
                    >
                      <ion-spinner 
                        class="button-loading-small"
                        v-if="state.creatingPost"
                        name="crescent"
                      />
                      <span v-else>
                        {{ state.uploadTitle }}
                      </span>
                    </ion-button>
                    <ion-button
                      size="small"
                      @click="clearPostForm"
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
import { UpdatePostVariables } from '@/mixims/interfaces'
import { useToastStore } from '@/stores/toast'
import { useCategoryInfoStore } from '@/stores/categoryInfo'
import { useUserStore } from '@/stores/user'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'

interface PostFileType {
  file: string
}

interface PostType {
  id: number,
  description: string,
  postfileSet: PostFileType[],
  category: {
    oftype: string
  }
}

const props = defineProps<{
  post?: PostType | null,
  type: string,
  showHeader?: Boolean,
  fixedPreviewHeight: Boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'postUpdated'): void;
  (e: 'postCreated'): void;
}>()

const state = reactive({
  // Post Information
  image: null,
  description: '',
  category: '',
  competition: '',
  oftype: '',

  preview: '',
  title: '',
  uploadTitle: '',
  refreshFileUpload: 0,
  creatingPost: false,
  uploadAction: () => {}
})

const toast = useToastStore()
const user = useUserStore()

if (props.type == 'create') {
  // Intialize create post data
  const { oftype, id, selectedComptn } = useCategoryInfoStore()
  state.oftype = oftype
  state.category = id
  state.competition = selectedComptn?.id || ''
} else if (props.post){
  // Post edit case
  state.oftype = props.post.category.oftype
}

function clearPostForm () {
  state.preview = ''
  state.image = null
  state.description = ''
  state.refreshFileUpload++
}

function createNewPost() {

  if (!user.success) {
    user.auth = true
    return
  }

  state.creatingPost = true

  let postVariables = {
    file: state.image || undefined,
    description: state.description,
    competition: state.competition || undefined,
    category: state.category
  }

  const { mutate, onDone, error: sendMessageError, onError } = useMutation(gql`    
    
    mutation ($file: Upload, $category: ID, $competition: ID, $description: String!) { 
      createPost (
        file: $file,
        competition: $competition,
        category: $category,
        description: $description
      ) {
          post {
            id
          }  
        }
    }

  `, () => ({
      variables: postVariables
    })
  )

  mutate()

  onDone(() => {
    state.creatingPost = false
    clearPostForm()
    emit('postCreated')
  })

  onError((error: any) => {
    state.creatingPost = false
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else {
      toast.$patch({message: 'Error Occured While Uploading Post', color: 'danger', open: true})
    }
  })
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
    const { mutate, onDone, onError } = useMutation(gql`    
    
      mutation ($id: ID!, $file: Upload, $description: String) { 
        updatePost (
          id: $id,
          file: $file,
          description: $description
        ) {
            post {
              id,
              description,
              postfileSet {
                file
              },
            }
          }
      }
    `,
      {
        variables
      }
    )
    
    mutate()

    onDone((value) => {
      emit('postUpdated')
    })

    onError((error: any) => {
      if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
        toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
      } else {
        toast.$patch({message: 'Error Occured While Updating Post', color: 'danger', open: true})
      }
    })
  }
}

function initialize() {
  if (props.type == 'edit' && props.post) {
    state.title = 'Edit Post'
    state.uploadTitle = 'Update'
    state.description = props.post.description
    props.post.postfileSet.length && (state.preview = `/media/${props.post.postfileSet[0].file}`)
    state.uploadAction = updatePost
  } else if (props.type == 'create') {
    state.title = 'Create Post'
    state.uploadTitle = 'Upload'
    state.uploadAction = createNewPost
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