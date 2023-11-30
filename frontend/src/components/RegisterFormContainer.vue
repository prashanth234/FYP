<template>

  <!-- Start of register form -->
  <form @submit.prevent="submitForm">
    <ion-grid v-show="!state.verify" class="register-form">

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
          <input
            id="recaptcha-verifier"
            type="submit"
            value="Register"
            class="auth-button"
            :class="{'disable-button': disableRegister}"
          >
          <!-- <ion-button
            v-show="state.loading"
            color="primary"
            class="auth-button"
            :disabled="true"
            expand="block"
          >
            <ion-spinner 
              class="button-loading-small"
              name="crescent"
            />
          </ion-button> -->
        </ion-col>

        <ion-col size="12" class="line" style="margin-top: 8px; margin-bottom: 15px;"></ion-col>

        <ion-col size="12">
          Have an account? <a class="cpointer" :class="{'cursor-disable': state.loading}" @click="goToLogin()"><b>Log in</b></a>
        </ion-col>

      </ion-row>

    </ion-grid>

    <div v-show="state.verify">
      <otp-container
        class="cpointer"
        :phone="fields.emailphone"
        @editphone="editphone"
        @submitOTP="submitOTP"
      />
    </div>
  </form>
  <!-- End of register form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonSpinner, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, inject, computed } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens, useAuth } from '@/composables/auth'
import { useAuthVerify } from '@/composables/authVerify'
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
const { fields, valid, getEmailOrPhone, emailphoneref, focusEmailPhone } = useAuth();
const { sendOTP, status, verifyOTP, firebaseSignOut } = useAuthVerify();

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

function isProcessing(value: boolean) {
  state.loading = value
  // Send processing state to parent
  isAuthProcessing(value)
}

async function submitOTP(otp: string, postVerify: any) {
  isProcessing(true)
  const response = await verifyOTP(otp)
  if (response.success) {
    // Register user
    register(response.user.accessToken, postVerify.bind(null, response))
  } else {
    // OTP verification failed
    postVerify(response)
    isProcessing(false)
  }
}

async function submitForm () {
  if (!valid.value.emailphone) {
    state.errors = ["Please enter valid email or phone"]
    return
  }

  state.errors = []
  isProcessing(true)

  const { phone } = getEmailOrPhone()

  if (phone) {
    checkUserDetails()
  } else {
    register()
  }
}

function register (token?: string, postRegister?: any) {

  const { mutate, onDone, onError } = useMutation(gql`
       mutation ($email: String, $phone: String, $username: String!, $password1: String!, $password2: String!, $token: String) {
        register (
          email: $email,
          phone: $phone,
          username: $username,
          password1: $password1,
          password2: $password2,
          token: $token
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
          ...getEmailOrPhone(),
          token
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  const errorToastMsg = 'User creation failed. Retry, or for assistance, please contact our support team.'

  onDone((result) => {
    isProcessing(false)
    const response = result.data.register
    if (response.errors) {
      authFailure('register')
      if (token) {
        // Mobile registration
        toast.$patch({message: errorToastMsg, color: 'danger', open: true})
      } else {
        // Email Registration
        const keys = Object.keys(response.errors)
        state.errors = []
        keys.forEach(key => {
          response.errors[key].forEach((response: {message: string}) => {
            state.errors.push(response.message)
          })
        })
      }
    } else if (response.success) {
      user.$patch({username: fields.username, auth: false, success: true})
      toast.$patch({message: "Success! You're now a valued member of our community.", color: 'success', open: true})
      user.getDetails()
      storeTokens(response, 'register')
      authSuccess('register')
      firebaseSignOut()
    }
    postRegister && postRegister()
  })

  onError(() => {
    isProcessing(false)
    authFailure('register')
    toast.$patch({message: errorToastMsg, color: 'danger', open: true})
    postRegister && postRegister()
  })
}

function checkUserDetails() {
  const emailOrPhone = getEmailOrPhone()

  const { mutate, onDone, onError } = useMutation(gql`
       query ($email: String, $phone: String, $username: String!, $password1: String!, $password2: String!) {
        userCheck (
          email: $email,
          phone: $phone,
          username: $username,
          password1: $password1,
          password2: $password2
        ) {
          success,
          errors
        }
      }
    `,{
        // Parameters
        variables: {
          username: fields.username,
          password1: fields.password1,
          password2: fields.password2,
          ...emailOrPhone,
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  onDone(async ({data}) => {
    if (data.userCheck.success) {
      if (emailOrPhone.phone) {
        const response = await sendOTP(emailOrPhone.phone)
        // Show verification popup
        response.success && (state.verify = true)
      } 
    } else {
      state.errors = data.userCheck.errors
    }
    isProcessing(false)
  })

  onError(() => {
    isProcessing(false)
  })
}
</script>

<style lang="scss" scoped>

.register-form {
  --ion-grid-column-padding: 6px;
}

.auth-button {
  width: 100%;
  border: 0px;
  background: var(--ion-color-primary);
  color: var(--ion-color-light);
  border-radius: 8px;
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
  &:hover {
    opacity: 0.92;
  }
  &.disable-button {
    cursor: default;
    opacity: 0.5;
    pointer-events: none;
  }
}

</style>