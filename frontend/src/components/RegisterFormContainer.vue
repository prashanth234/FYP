<template>

  <!-- Start of register form -->
  <form @submit.prevent="submitForm">
    <ion-grid v-if="!state.verify" class="register-form">

      <ion-row class="ion-text-center">
        
        <ion-col size="12" class="ion-padding-bottom" style="font-size: 20px; font-weight: 600;">
          Create Account
        </ion-col>

        <ion-col size="12">
          <ion-input 
            class="custom-input"
            v-model="fields.emailphone"
            type="text"
            placeholder="Email or Phone"
            required
            ref="emailphoneref"
            autofocus
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="fields.username"
            type="text"
            placeholder="Username"
            autocomplete="username"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="fields.password1"
            type="password"
            placeholder="Password"
            autocomplete="new-password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="fields.password2"
            type="password"
            placeholder="Confirm Password"
            autocomplete="new-password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12" class="ion-no-padding">
          <errors :errors="state.errors"/>
        </ion-col>

        <ion-col size="12">
          <ion-button color="primary" class="auth-button" :disabled="disableRegister" expand="block" type="submit">
            <ion-spinner 
              class="button-loading-small"
              v-if="state.loading"
              name="crescent"
            />
            <span v-else>
              Register
            </span>
          </ion-button>
        </ion-col>

        <ion-col size="12" class="line" style="margin-top: 8px; margin-bottom: 15px;"></ion-col>

        <ion-col size="12">
          Have an account? <a class="cpointer" :class="{'cursor-disable': state.loading}" @click="goToLogin()"><b>Log in</b></a>
        </ion-col>

      </ion-row>

    </ion-grid>

    <div v-else="state.verify">
      <otp-container
        class="cpointer"
        :phone="fields.emailphone"
        @editphone="editphone"
      />
    </div>
  </form>
  <!-- End of register form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonText, IonSpinner, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, inject, computed, ref, nextTick } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens, useAuth } from '@/composables/auth'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'
import errors from './errorContainer.vue'
import OtpContainer from './OTPContainer.vue'

const emit = defineEmits<{
  (e: 'changeform', to: string): void
}>()

const { isAuthProcessing, authSuccess, authFailure } = inject<any>('auth')

interface State {
  errors: Array<string>,
  loading: boolean,
  isOpen: boolean,
  verify: boolean
}

const state: State = reactive({
  loading: false,
  isOpen: false,
  errors: [],
  verify: false
})

const ionRouter = useIonRouter();
const toast = useToastStore();
const user = useUserStore();
const {fields, valid, getEmailOrPhone, emailphoneref, focusEmailPhone} = useAuth();

fields.emailphone = '7097904099'
fields.username = 'prashanth123'
fields.password1 = 'prashanth123'
fields.password2 = 'prashanth123'

const disableRegister = computed(() => {
  return state.loading
})

function goToLogin() {
  emit('changeform', 'login')
}

function editphone() {
  state.verify = false
  focusEmailPhone()
}

function submitForm () {
  if (!valid.value.emailphone) {
    state.errors = ["Please enter valid email or phone"]
    return
  }

  state.errors = []

  const { phone } = getEmailOrPhone()

  if (phone) {
    state.verify = true
  } else {
    register()
  }

}

function register () {

  state.loading = true
  isAuthProcessing(true)

  const { mutate, onDone, onError } = useMutation(gql`
       mutation ($email: String, $phone: String, $username: String!, $password1: String!, $password2: String!) {
        register (
          email: $email,
          phone: $phone,
          username: $username,
          password1: $password1,
          password2: $password2,
        ) {
          success,
          errors,
          token,
          refreshToken
        }
      }
    `,{
        // Parameters
        variables: {
          username: fields.username,
          password1: fields.password1,
          password2: fields.password2,
          ...getEmailOrPhone()
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  onDone((result) => {
    state.loading = false
    authFailure('register')
    const response = result.data.register
    if (response.errors) {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach((response: {message: string}) => {
          state.errors.push(response.message)
        })
      })
    } else if (response.success) {
      user.$patch({username: fields.username, auth: false, success: true})
      toast.$patch({message: "Success! You're now a valued member of our community.", color: 'success', open: true})
      user.getDetails()
      storeTokens(response, 'register')
      authSuccess('register')
    }
  })

  onError(() => {
    state.loading = false
    authFailure('register')
    toast.$patch({message: 'User creation failed. Retry, or for assistance, please contact our support team.', color: 'danger', open: true})
  })
}
</script>

<style lang="scss" scoped>

.register-form {
  --ion-grid-column-padding: 6px;
}

</style>