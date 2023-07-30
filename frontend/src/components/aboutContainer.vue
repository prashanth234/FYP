<template>
  <ion-row class="ion-justify-content-center">
    <ion-col size="auto">
      <file-upload-container
        v-model="state.image"
        @update:preview="imageSelected"
        :key="state.refreshFileUpload"
        :simple="true"
        :cropable="true"
      >
        <template #handler="{selectImage}">
          <ion-avatar style="width: 90px; height: 90px;" class="cpointer" @click="selectImage">
            <img
              alt="http://localhost:8000/static/avatar.svg"
              :src="result?.me.avatar ? `http://localhost:8000/media/${result.me.avatar}?temp=${user.userUpdated}` : 'http://localhost:8000/static/avatar.svg'"
            />
          </ion-avatar>
          <div class="camera-icon">
            <ion-icon :icon="cameraOutline"></ion-icon>
          </div>
        </template>
      </file-upload-container>
    </ion-col>
  </ion-row>

  <ion-list>

    <ion-item>
      <ion-input label="Username" :value="result?.me.username" :disabled="true" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input label="Email" :value="result?.me.email" :disabled="true" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="state.firstName" label="First Name" labelPlacement="floating" placeholder="Enter here"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="state.lastName" label="Last Name" labelPlacement="floating" placeholder="Enter here"></ion-input>
    </ion-item>

    <ion-item>
      <ion-select v-model="state.gender" label="Gender" label-placement="floating">
        <ion-select-option value="M">Male</ion-select-option>
        <ion-select-option value="F">Female</ion-select-option>
        <ion-select-option value="O">Others</ion-select-option>
      </ion-select>
    </ion-item>

  </ion-list>

  <ion-row>
    <ion-col size="12">
      <ion-button
        color="primary"
        style="float: right"
        @click="updateProfile"
        :disabled="state.loading"
      >
        <ion-spinner 
            class="button-loading-small"
            v-if="state.loading"
            name="crescent"
          />
          <span v-else>
            Update
          </span>
      </ion-button>
      <!-- <ion-button
        color="light"
        style="float: right; margin-right: 15px;"
      >
        Cancel
      </ion-button> -->
    </ion-col>
  </ion-row>

</template>

<script setup lang="ts">
import { IonAvatar, IonIcon, IonList, IonItem, IonInput, IonRow, IonCol, IonButton, IonSelect, IonSelectOption, IonSpinner } from '@ionic/vue'
import { CropperResult } from 'vue-advanced-cropper'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive } from 'vue'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { cameraOutline } from 'ionicons/icons'
import store from '@/vuex';
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

interface State {
  image: null,
  preview: string,
  refreshFileUpload: number,
  firstName: string,
  lastName: string,
  gender: string,
  loading: boolean
}


const state: State = reactive({
  image: null,
  preview: '',
  refreshFileUpload: 0,
  firstName: '',
  lastName: '',
  gender: '',
  loading: false
})

const user = useUserStore();
const toast = useToastStore();

// Profile image

function imageSelected(blob: CropperResult, type: string) {
  try {
    const { mutate, onDone } = useMutation(gql`    
      mutation ($avatar: Upload!, $type: String!) { 
        updateAvatar (
          avatar: $avatar,
          type: $type
        ) {
            user {
              avatar
            }
          }
      }
    `,
      {
        variables: {
          avatar: state.image,
          type
        },
      }
    )
    mutate()
    onDone((value) => {
      user.userUpdated += 1
    })
  } catch (error) {
    console.error(error)
  }
}

function updateProfile () {
  const {firstName, lastName, gender} = state

  state.loading = true

  try {
    const { mutate, onDone } = useMutation(gql`    
      mutation ($gender: String, $firstName: String, $lastName: String, $dateOfBirth: String) { 
        updateAccount (
          gender: $gender,
          firstName: $firstName,
          lastName: $lastName,
          dateOfBirth: $dateOfBirth
        ) {
            success,
            errors
          } 
      }
    `,
      {
        variables: {
          firstName,
          lastName,
          gender
        },
      }
    )
    mutate()
    onDone((value) => {
      toast.$patch({message: 'Update Successful', color: 'success', open: true})
      state.loading = false
    })
  } catch (error) {
    console.error(error)
    state.loading = false
  }
}

const { result, onResult } = useQuery(gql`   
                              query {
                                me {
                                  username,
                                  firstName,
                                  lastName,
                                  email,
                                  gender,
                                  dateOfBirth,
                                  avatar
                                }
                              }
                            `)

onResult(({data, loading}) => {
  if (loading) return
  const { firstName, lastName, gender } = data.me
  state.firstName = firstName
  state.lastName = lastName
  state.gender = gender
})

</script>

<style lang="scss" scoped>
.camera-icon {
  position: relative;
  left: 58px;
  bottom: 25px;
  background-color: white;
  color: black;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 50%;
  padding: 6px;
}
</style>