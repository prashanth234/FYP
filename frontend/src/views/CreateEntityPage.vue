<template>

  <ion-page>
    <ion-content>

      <form @submit.prevent="submit" id="login-form">

        <ion-grid class="create-entity-grid card">
          <ion-row class="ion-justify-content-center ion-text-center">

            <!-- Title -->
            <ion-col size="12">
              <div style="font-size: 22px; font-weight: 590;">
                {{ props.editId ? 'Edit Entity' : 'Request Entity' }}
              </div>
              <div v-if="!props.editId" style="font-size: 15px; padding: 5px 0px;">
                Be the one to represent your entity
              </div>
            </ion-col>

            <!-- Image -->
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
                    <img v-else-if="state.image" class="image" :src="state.image" alt="" />
                    <ion-icon v-else class="default-entity" :icon="businessOutline"></ion-icon>
                  </ion-avatar>
                  <div class="upload-camera-icon">
                    <ion-icon :icon="cameraOutline"></ion-icon>
                  </div>
                </template>
              </FileUpload>
            </ion-col>

            <!-- Name -->
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

            <!-- Description -->
            <ion-col size="12">
              <ion-input
                class="custom-input"
                v-model="state.description"
                type="text"
                placeholder="Description"
              >
              </ion-input>
            </ion-col>
            
            <!-- Entity Type -->
            <ion-col size="12" class="ion-text-start" v-if="!props.editId">
              <ion-select
                class="custom-select"
                v-model="state.type"
                @ionChange="onTypeChange"
                placeholder="Type"
                label-placement="stacked"
                interface="popover"
                required
              >
                <select v-if="!state.type" slot="end" required class="select-required"></select>
                  <ion-select-option
                    v-for="(entity, index) in state.entities"
                    :value="entity"
                    :key="index"
                  >
                    {{ entity }}
                  </ion-select-option>
              </ion-select>
            </ion-col>

            <!-- Entity Type Others -->
            <ion-col size="12" v-if="state.type == 'Others' && !props.editId" >
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

            <!-- City -->
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

            <ion-col v-if="props.editId" size="12" class="ion-no-padding ion-text-start">

              <ion-row>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.maps"
                    type="text"
                    placeholder="Maps Link"
                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.phone"
                    type="tel"
                    placeholder="WhatsApp"
                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.email"
                    type="email"
                    placeholder="Email"
                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.instagram"
                    type="text"
                    placeholder="Instagram"                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.facebook"
                    type="text"
                    placeholder="Facebook"
                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-input
                    class="custom-input"
                    v-model="state.linkedin"
                    type="text"
                    placeholder="Linkedin"
                  >
                  </ion-input>
                </ion-col>

                <ion-col size="12">
                  <ion-select
                    :multiple="true"
                    class="custom-select"
                    v-model="state.admins"
                    placeholder="Admins"
                    label-placement="stacked"
                    interface="popover"
                    required
                  >
                    <ion-select-option
                      v-for="(user, index) in state.users"
                      :value="user"
                      :key="index"
                    >
                      {{ user.username }}
                    </ion-select-option>
                  </ion-select>
                  <div v-if="!state.admins.length" class="error-msg">
                    Please pick at least one admin.
                  </div>
                </ion-col>

              </ion-row>

            </ion-col>
            
            <!-- ID Upload -->
            <ion-col size="12" v-if="!props.editId">
              <div style="padding-bottom: 10px;">
                Upload any ID that shows you belong to the entity
              </div>
              <FileUpload
                v-model="state.proof"
                @update:preview="onProofSelect"
                :simple="true"
                :cropable="false"
                file-type="image/*"
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

            <!-- Errors -->
            <div :class="{'errors-div': state.errors.length}">
              <errors :errors="state.errors"/>
            </div>

            <!-- Submit -->
            <ion-col size="12">

              <ion-button
                color="success"
                size="small"
                style="width: 200px;"
                :disabled="disableSubmit"
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
import { ref, watch, computed } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { cameraOutline, businessOutline, checkmarkCircleOutline } from 'ionicons/icons'
import { Preview, CropperResult } from 'vue-advanced-cropper'
import { useToastStore } from '@/stores/toast'
import errors from '@/components/ErrorContainer.vue'
import FileUpload from '@/components/FileUploadContainer.vue'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { useDialogStore } from '@/stores/dialog'
import { useEntityInfoStore } from '@/stores/entityInfo'
import { pick, differenceByValue } from '@/utils/common'
import { UserType} from '@/utils/interfaces'

const props = defineProps({
  editId: String
})

const route = useRoute()

interface State {
  id?: string,
  edit: boolean,
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
  instagram: string,
  facebook: string,
  linkedin: string,
  phone: string,
  email: string,
  maps: string,
  entities: string[],
  admins: UserType[],
  users: UserType[]
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
  instagram: '',
  facebook: '',
  linkedin: '',
  phone: '',
  email: '',
  maps: '',
  edit: false,
  // Also update entites in backend
  entities: [
    "School",
    "College",
    "Institute",
    "Others"
  ],
  admins: [],
  users: []
}

const state = ref<State>({...intialState})

const disableSubmit = computed(() => {
  const data = state.value
  if (props.editId) {
    return data.loading || !data.admins.length
  } else {
    return data.loading
  }
})

const editProperties: (keyof State)[] = ['name', 'description', 'instagram', 'facebook', 'linkedin', 'phone', 'email', 'image', 'city', 'maps']
let orginalData: any = {}

// When page is opended again for edit, model data needed to be updated
watch(() => route.params.editId, () => {
  if (route.name == 'editEntity' && route.params.editId == props.editId) {
    getEntityDetails()
  }
})

// On first time page load
props.editId && getEntityDetails()

onBeforeRouteLeave(() => {
  Object.assign(state.value, {...intialState, users: [], admins: [], errors: []}),
  orginalData = {}
})

const toast = useToastStore()
const ionRouter = useIonRouter()
const dialog = useDialogStore()

const TYPE_ERROR = 'Please select the entity type.'
const PROOF_ERROR = 'Please upload ID to continue.'

function createEntityDetails() {
  state.value.errors = []

  if (!state.value.type || !state.value.city || !state.value.proof) {
    !state.value.type && state.value.errors.push(TYPE_ERROR)
    !state.value.proof && state.value.errors.push(PROOF_ERROR)
    return
  }

  state.value.loading = true

  const { name, description, type: entityType, otherType, image, city, proof } = state.value

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
      state.value.errors.push(data.createEntity.message)
    }
    state.value.loading = false
  })

  onError(() => {
    toast.$patch({message: 'Failed to process request, please try again.', color: 'danger', open: true})
    state.value.loading = false
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
  state.value.otherType = ''
  removeError(TYPE_ERROR)
}

function onProofSelect() {
  removeError(PROOF_ERROR)
}

function removeError(error: string) {
  state.value.errors = state.value.errors.filter(item => item != error)
}

function submit() {
  if (props.editId) {
    updateEntityDetails()
  } else {
    createEntityDetails()
  }
}

////////////// EDIT //////////////

function getEntityDetails(){
  const entity = useEntityInfoStore()
  // Update the local state
  Object.assign(state.value, entity.details)
  // Store original data of later reference during api update
  orginalData = pick(state.value, editProperties)
  entity.details.id && getEntityUsers(entity.details.id)
  entity.$reset()
}

function getEntityUsers(id: string) {
  const QUERY = gql `
    query ($id: ID!) { 
      entityUsers (id: $id) {
        id,
        username
      }
    }
  `
  const { onResult, onError } = useQuery(QUERY, () => ({
    id
  }))

  onResult(({data, loading}) => {
    if (!loading) {
      const admins: UserType[] = []
      orginalData.adminIds = new Set(state.value.admins.map((user: UserType) => user.id))
      data.entityUsers.forEach((user: UserType) => {
        orginalData.adminIds.has(user.id) && (admins.push(user))
        state.value.users.push(user)
      })
      state.value.admins = admins
    }
  })
  
  onError(() => {
  })
}

function updateEntityDetails(){

  state.value.errors = []

  const variables = differenceByValue(orginalData, state.value, editProperties)

  // Admins
  const admins: string[] = []
  let sameAdmins = (state.value.admins.length == orginalData.adminIds.length)

  state.value.admins.forEach((admin: UserType) => {
    !orginalData.adminIds.has(admin.id) && (sameAdmins = false)
    admins.push(admin.id)
  })
  
  !sameAdmins && (variables.admins = admins)

  const keys = Object.keys(variables)
  
  if (!keys.length) {
    toast.$patch({message: 'Everything looks good—no updates found!', color: 'primary', open: true})
    return
  }

  variables.id = state.value.id

  const { mutate, onDone, onError } = useMutation(gql`    
    
    mutation editEntity ($id: String!, $name: String, $description: String, $image: Upload, $city: String, $instagram: String, $facebook: String, $linkedin: String, $phone: String, $email: String, $maps: String, $admins: [ID]) { 
      editEntity (
        id: $id,
        name: $name,
        description: $description,
        image: $image,
        city: $city,
        instagram: $instagram,
        facebook: $facebook,
        linkedin: $linkedin,
        phone: $phone,
        email: $email,
        maps: $maps,
        admins: $admins
      ) {
          success,
          details {
            id,
            isAdmin,
            ${keys.join().replace('admins', 'admins { id, username }')}
          },
          message
        }
    }

  `, () => ({
      variables: variables
    })

  )

  mutate()

  onDone(({data}) => {
    if (data.editEntity.success) {
      toast.$patch({message: 'Your entity information has been updated successfully!', color: 'success', open: true})
      ionRouter.back()
    } else {
      state.value.errors.push(data.editEntity.message)
    }
    state.value.loading = false
  })

  onError(() => {
    toast.$patch({message: 'Failed to process request, please try again.', color: 'danger', open: true})
    state.value.loading = false
  })
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
  border: 1px solid var(--ion-color-dark);
  border-radius: 50%;
}

.errors-div {
  padding: 0px 15px;
}
.select-required {
  border: 0px;
  appearance: none;
  background-color: transparent;
  outline: none;
  width: 1px;
  /* for Firefox */
  -moz-appearance: none;
  /* for Chrome */
  -webkit-appearance: none;
}
.error-msg {
  margin-top: 5px;
  margin-left: 2px;
  color: var(--ion-color-danger-tint);
}
</style>