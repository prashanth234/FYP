<template>

  <ion-page>
    <ion-content>

      <form @submit.prevent="submit" id="login-form">

        <ion-grid class="create-entity-grid card">
          <ion-row class="ion-justify-content-center ion-text-center">

            <ion-col size="12">
              <div style="font-size: 22px; font-weight: 590;">Request Entity</div>
              <div style="font-size: 15px; padding: 5px 0px;">Be the one to represent your entity</div>
            </ion-col>

            <ion-col size="auto">
              <FileUpload
                v-model:preview="state.imagePreview"
                v-model="state.image"
                :simple="true"
                :cropable="true"
              >
                <template #handler="{selectImage}">
                  <ion-avatar style="width: 100px; height: 100px;" class="cpointer" @click="selectImage">
                    <preview
                      v-if="state.imagePreview"
                      :width="100" :height="100"
                      style="border-radius: 50%;"
                      :image="state.imagePreview.image"
                      :coordinates="state.imagePreview.coordinates"
                    />
                    <ion-icon v-else class="default-entity" :icon="businessOutline"></ion-icon>
                  </ion-avatar>
                  <div class="upload-camera-icon">
                    <ion-icon :icon="cameraOutline"></ion-icon>
                  </div>
                </template>
              </FileUpload>
            </ion-col>

            <ion-col size="12">
              <ion-input
                class="custom-input"
                v-model="state.name"
                type="text"
                placeholder="Name"
                required
              >
              </ion-input>
            </ion-col>

            <ion-col size="12">
              <ion-input
                class="custom-input"
                v-model="state.description"
                type="text"
                placeholder="Description"
              >
              </ion-input>
            </ion-col>
            
            <ion-col size="12" class="ion-text-start">
              <ion-select
                class="custom-select"
                v-model="state.type"
                @ionChange="onTypeChange"
                placeholder="Type"
                label-placement="stacked"
                interface="popover"
                required
              >
                <ion-select-option
                  v-for="(entity, index) in state.entities"
                  :value="entity"
                  :key="index"
                >
                  {{ entity }}
                </ion-select-option>
              </ion-select>
            </ion-col>

            <ion-col size="12" v-if="state.type == 'Others'">
              <ion-input
                class="custom-input"
                v-model="state.otherType"
                type="text"
                placeholder="Enter Entity Type"
                required
              >
              </ion-input>
            </ion-col>

            <!-- <ion-col size="12" class="ion-text-start">
              <ion-select
                class="custom-select"
                v-model="state.city"
                @ionChange="onCityChange"
                placeholder="City"
                label-placement="stacked"
                interface="popover"
                required
              >
                <ion-select-option value="OTHERS">Others</ion-select-option>
              </ion-select>
            </ion-col> -->

            <ion-col size="12">
              <ion-input
                class="custom-input"
                v-model="state.city"
                type="text"
                placeholder="City"
                required
              >
              </ion-input>
            </ion-col>
            
            <ion-col size="12">
              <div style="padding-bottom: 10px;">
                Upload any ID that shows you belong to the entity
              </div>
              <FileUpload
                v-model="state.proof"
                @update:preview="onProofSelect"
                :simple="true"
                :cropable="false"
                file-type="image/*,.pdf"
              >
                <template #handler="{selectImage, loading}">
                  <ion-button
                    @click="selectImage()"
                    for="file-upload"
                    size="small"
                    fill="outline"
                    color="primary"
                    :disabled="loading || state.loading"
                  >
                    <ion-spinner 
                      class="button-loading-small"
                      v-if="loading"
                      name="crescent"
                    />
                    <span v-else>
                      Upload File
                    </span>
                  </ion-button>
                </template>
              </FileUpload>

              <div class="uploaded-filename">
                {{ state.proof ? state.proof.name : '' }}
              </div>
              
            </ion-col>

            <div :class="{'errors-div': state.errors.length}">
              <errors :errors="state.errors"/>
            </div>

            <ion-col size="12">

              <ion-button
                color="success"
                size="small"
                style="width: 200px;"
                :disabled="state.loading"
                type="submit"
              >
                <ion-spinner 
                  class="button-loading-small"
                  v-if="state.loading"
                  name="crescent"
                />
                <span v-else>
                  Submit
                </span>
              </ion-button>

            </ion-col>

          </ion-row>
        </ion-grid>

      </form>

    </ion-content>
  </ion-page>

</template>

<script lang="ts" setup>
import { IonSelect, useIonRouter, IonSelectOption, IonGrid, IonPage, IonContent, IonInput, IonAvatar, IonIcon, IonRow, IonCol, IonButton, IonSpinner, IonCard } from '@ionic/vue'
import { reactive } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { cameraOutline, businessOutline, checkmarkCircleOutline } from 'ionicons/icons'
import { Preview, CropperResult } from 'vue-advanced-cropper'
import { useToastStore } from '@/stores/toast'
import errors from '@/components/ErrorContainer.vue'
import FileUpload from '@/components/FileUploadContainer.vue'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useDialogStore } from '@/stores/dialog'


interface State {
  name: string,
  description: string,
  type: string,
  otherType: string,
  image: null,
  city: string,
  cityOthers: string,
  loading: boolean,
  errors: string[],
  proof: any,
  imagePreview: CropperResult | undefined,
  entities: string[]
}

const intialState: State = {
  name: '',
  description: '',
  type: '',
  otherType: '',
  image: null,
  city: '',
  cityOthers: '',
  loading: false,
  errors: [],
  proof: undefined,
  imagePreview: undefined,
  // Also update entites in backend
  entities: [
    "School",
    "College",
    "Institute",
    "Others"
  ]
}

const state: State = reactive({...intialState})

onBeforeRouteLeave(() => {
  Object.assign(state, intialState)
})

const toast = useToastStore()
const ionRouter = useIonRouter()
const dialog = useDialogStore()

const TYPE_ERROR = 'Please select the entity type.'
const PROOF_ERROR = 'Please upload ID to continue.'

function submit() {
  state.errors = []

  if (!state.type || !state.city || !state.proof) {
    !state.type && state.errors.push(TYPE_ERROR)
    !state.proof && state.errors.push(PROOF_ERROR)
    return
  }

  state.loading = true

  const { name, description, type: entityType, otherType, image, city, proof } = state

  let variables = {
    name, description, image, proof, city, entityType, otherType, type: entityType
  }

  const { mutate, onDone, onError } = useMutation(gql`    
    
    mutation createEntity ($name: String!, $description: String, $image: Upload, $proof: Upload!, $type: String!, $city: String!, $otherType: String) { 
      createEntity (
        name: $name,
        description: $description,
        image: $image,
        proof: $proof,
        type: $type,
        city: $city,
        otherType: $otherType
      ) {
          success,
          message
        }
    }

  `, () => ({
      variables: variables
    })

  )

  mutate()

  onDone(({data}) => {
    if (data.createEntity.success) {
      showSuccessPopup(data.createEntity.message)
    } else {
      state.errors.push(data.createEntity.message)
    }
    state.loading = false
  })

  onError(() => {
    toast.$patch({message: 'Failed to process request, please try again.', color: 'danger', open: true})
    state.loading = false
  })
  
}

function showSuccessPopup(message: string) {
  const buttons = [
    {title: 'Okay', color: 'primary', action: 'send', control: routerToEntity}
  ]

  const description =  message

  dialog.show(
    '',
    description,
    buttons,
    checkmarkCircleOutline,
    'success'
  )
}

function routerToEntity() {
  dialog.close()
  ionRouter.push('/entity')
}

function onTypeChange() {
  state.otherType = ''
  removeError(TYPE_ERROR)
}

function onProofSelect() {
  removeError(PROOF_ERROR)
}

function removeError(error: string) {
  state.errors = state.errors.filter(item => item != error)
}

</script>

<style lang="scss">

.create-entity-grid {
  max-width: 500px;
  --ion-grid-padding: 20px;
}

.default-entity {
  font-size: 55px;
  padding: 20px;
  border: 1px solid white;
  border-radius: 50%;
}

.errors-div {
  padding: 0px 15px;
}

</style>