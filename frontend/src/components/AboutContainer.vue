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
              alt="avatar"
              :src="userAvatar"
            />
          </ion-avatar>
          <div class="upload-camera-icon">
            <ion-icon :icon="cameraOutline"></ion-icon>
          </div>
        </template>
      </file-upload-container>
    </ion-col>
  </ion-row>

  <ion-list>

    <ion-item>
      <ion-input label="Username" :value="user.username" :disabled="true" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item v-if="user.email">
      <ion-input :disabled="user.verified" label="Email" inputmode="email" v-model="fields.email" labelPlacement="floating"></ion-input>
    </ion-item>

    <div class="ion-text-end cpointer" v-if="user.email && !user.verified">
      <a @click="verifyEmail">Verify Email</a>
    </div>

    <ion-item v-if="user.phone">
      <ion-input :disabled="user.verified" label="Phone" inputmode="tel" type="tel" v-model="fields.phone" labelPlacement="floating"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="fields.firstName" label="First Name" labelPlacement="floating" placeholder="Enter here"></ion-input>
    </ion-item>

    <ion-item>
      <ion-input v-model="fields.lastName" label="Last Name" labelPlacement="floating" placeholder="Enter here"></ion-input>
    </ion-item>

    <ion-item>
      <ion-select v-model="fields.gender" label="Gender" label-placement="floating" interface="popover">
        <ion-select-option value="M">Male</ion-select-option>
        <ion-select-option value="F">Female</ion-select-option>
        <ion-select-option value="O">Others</ion-select-option>
      </ion-select>
    </ion-item>

    <!-- <ion-item>
      <ion-input class="custom-input" v-model="state.dob" @click="controlDOB(true)" type="text" placeholder="Birth Date"></ion-input>
      <ion-popover :is-open="state.isOpen">
        <ion-datetime @ionCancel="controlDOB(false)" @ionChange="changeDOB" :show-default-buttons="true" presentation="date"></ion-datetime>
      </ion-popover>
    </ion-item> -->

    <div class="ion-padding-horizontal">
      <errors :errors="state.errors"/>
    </div>

  </ion-list>

  <ion-row>
    <ion-col size="12">
      <ion-button
        color="primary"
        class="float-right"
        @click="updateProfile"
        :disabled="state.loading"
        size="small"
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
    </ion-col>
  </ion-row>

</template>

<script setup lang="ts">
import { IonAvatar, IonIcon, IonList, IonItem, IonInput, IonRow, IonCol, IonButton, IonSelect, IonSelectOption, IonSpinner, IonText } from '@ionic/vue'
import { CropperResult } from 'vue-advanced-cropper'
import FileUploadContainer from '@/components/FileUploadContainer.vue'
import { reactive, computed, watch } from 'vue'
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { cameraOutline, alertCircleOutline } from 'ionicons/icons'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useUserFields } from '@/composables/auth'
import { useDialogStore } from '@/stores/dialog'
import errors from './ErrorContainer.vue'

interface State {
  image: null,
  preview: string,
  refreshFileUpload: number,
  loading: boolean,
  errors: string[]
}

const state: State = reactive({
  image: null,
  preview: '',
  refreshFileUpload: 0,
  loading: false,
  errors: []
})

const user = useUserStore();
const toast = useToastStore();
const {fields, valid, error} = useUserFields();
const dialog = useDialogStore();

watch(() => user.username, setUserState)

function setUserState() {
  const { firstName, lastName, gender, email, phone } = user
  fields.firstName = firstName
  fields.lastName = lastName
  fields.gender = gender
  fields.email = email
  fields.phone = phone
}

setUserState()

const userAvatar = computed(() => {
  return user.avatar || '/static/core/avatar.svg'
})

// Profile image

function imageSelected(blob: CropperResult, type: string) {
  const { mutate, onDone, onError } = useMutation(gql`    
    mutation updateAvatar ($avatar: Upload!, $type: String!) { 
      updateAvatar (
        avatar: $avatar,
        type: $type
      ) {
          user {
            id,
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

  onDone(({data}) => {
    user.$patch({avatar: data.updateAvatar.user.avatar, userUpdated: user.userUpdated + 1})
  })

  onError((error: any) => {
    if (error?.networkError?.response?.statusText == 'Request Entity Too Large') {
      toast.$patch({message: 'Request Entity Too Large', color: 'danger', open: true})
    } else {
      toast.$patch({message: 'Error Occured While Updating Profile', color: 'danger', open: true})
    }
  })
}

function updateProfile () {
  state.errors = []

  const {firstName, lastName, gender} = fields

  // if (!email && !phone) {
  //   state.errors.push('Please provide either email or phone number')
  // } else {
  //   if (email && !valid.value.email) {
  //     state.errors.push('Please enter a valid email')
  //   } else if (phone && !valid.value.phone) {
  //     state.errors.push('Please enter a valid phone number')
  //   }
  // }

  if (state.errors.length) { return }

  state.loading = true

  const { mutate, onDone, onError } = useMutation(gql`    
    mutation ($gender: String, $firstName: String, $lastName: String) { 
      updateAccount (
        gender: $gender,
        firstName: $firstName,
        lastName: $lastName
      ) {
          success
        } 
    }
  `,
    {
      variables: {
        firstName: firstName,
        lastName: lastName,
        gender: gender,
        // email: email != user.email ? email : undefined,
        // phone: phone != user.phone ? phone : undefined
      },
    }
  )

  mutate()

  onDone(({data}) => {
    toast.$patch({message: "Success! Your user account has been updated.", color: 'success', open: true})
    data.updateAccount.success && user.$patch({firstName, lastName, gender})
    state.loading = false
  })

  onError((error: any) => {
    state.loading = false
    if (error?.graphQLErrors[0]?.message) {
      state.errors.push(error.graphQLErrors[0].message)
    } else {
      toast.$patch({message: 'Profile update failed due to an error. Please attempt again.' , color: 'danger', open: true})
    }
  })
}

function sendVerificationEmail () {
  const { mutate, onDone, onError } = useMutation(gql`    
    mutation ($email: String!) { 
      resendActivationEmail (
        email: $email
      ) {
          success,
          errors
        }
    }
  `,
    {
      variables: {
        email: user.email
      },
    }
  )

  mutate()
  toast.$patch({message: 'Success! A verification email is heading to your inbox.', color: 'success', open: true})
  dialog.close()
}

function verifyEmail () {
  const buttons = [
    {title: 'Resend', color: 'primary', action: 'send', control: sendVerificationEmail},
    {title: 'Cancel', color: 'light'}
  ]

  const description = `Verification email has been sent to your email account (${user.email}). If not received, please click the 'Resend' button.`

  dialog.show(
    '',
    description,
    buttons,
    alertCircleOutline,
    'primary'
  )
}

// interface DatetimeChangeEventDetail {
//   detail: {
//     value: string
//   }
// }

// function controlDOB(value: boolean) {
//   state.isOpen = value
// }

// function changeDOB(event: DatetimeChangeEventDetail) {
//   state.dob = event.detail.value.substring(0, 10)
//   controlDOB(false)
// }
</script>

<style lang="scss" scoped>
ion-item {
  &::part(native) {
    padding-left: 2px;
  }
}
</style>