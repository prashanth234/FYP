<template>

  <!-- Start of register form -->
  <form @submit.prevent="submitForm" id="register-form">
    <ion-grid class="register-form">

      <ion-row class="ion-text-center">
        
        <ion-col
          size="12"
          class="ion-padding-bottom auth-header"
        >
          Create Account
        </ion-col>

        <ion-col size="12">
          <ion-input 
            class="custom-input"
            v-model="auth.fields.emailphone"
            type="text"
            placeholder="Email or IN Phone"
            required
            ref="emailphoneref"
            autofocus
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="auth.fields.username"
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
            v-model="auth.fields.password1"
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
            v-model="auth.fields.password2"
            type="password"
            placeholder="Confirm Password"
            autocomplete="new-password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12" class="ion-no-padding">
          <errors :errors="auth.errors"/>
        </ion-col>

        <ion-col size="12">
          <input
            id="recaptcha-verifier"
            type="submit"
            value="Register"
            class="auth-button input-auth-button"
            :class="{'disable-button': auth.processing}"
          >
        </ion-col>

        <ion-col size="12" class="line" style="margin-top: 8px; margin-bottom: 15px;"></ion-col>

        <ion-col size="12">
          Have an account? <a class="cpointer auth-link" :class="{'cursor-disable': auth.processing}" @click="goToLogin()"><b>Log in</b></a>
        </ion-col>

      </ion-row>

    </ion-grid>
  </form>
  <!-- End of register form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput } from '@ionic/vue'
import gql from 'graphql-tag'
import { useMutation } from '@vue/apollo-composable'
import { useAuth, useRecaptchaVerifier, useEmailPhoneFocus } from '@/composables/auth'
import { useToastStore } from '@/stores/toast'
import errors from './ErrorContainer.vue'
import { useAuthStore } from '@/stores/auth'

const toast = useToastStore();
const auth = useAuthStore();
const { firebaseSignOut } = useAuth();
const { emailphoneref } = useEmailPhoneFocus();

useRecaptchaVerifier()

// auth.fields.emailphone = 'prashanth.bobby89@gmail.com'
// auth.fields.username = 'prashanth123a'
// auth.fields.password1 = 'prashanth123'
// auth.fields.password2 = 'prashanth123'

function goToLogin() {
  auth.discardMessage()
  auth.changeForm('login')
}

async function submitForm () {
  if (!auth.isValidEmailPhone()) {
    return
  }

  auth.processState(true)

  if (auth.isInputPhone) {
    checkUserDetails()
  } else {
    register()
  }
}

function register (user?: any) {

  const token = user ? user.accessToken : undefined

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
          errors
        }
      }
    `,{
        // Parameters
        variables: {
          username: auth.fields.username,
          password1: auth.fields.password1,
          password2: auth.fields.password2,
          ...auth.emailOrPhone,
          token
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  const errorToastMsg = 'User creation failed. Retry, or for assistance, please contact our support team.'

  onDone((result) => {
    auth.processState(false)
    const response = result.data.register
    if (response.errors) {
      if (token) {
        // Mobile registration
        toast.$patch({
            message: errorToastMsg,
            color: 'danger',
            open: true
          })
      } else {
        // Email Registration
        const keys = Object.keys(response.errors)
        keys.forEach(key => {
          response.errors[key].forEach((response: {message: string}) => {
            auth.errors.push(response.message)
          })
        })
      }
    } else if (response.success) {
      if (token) {
        // Mobile registration
        auth.showMessage("Success! You're now a valued member of our community. Please Log In.", 'success')
        
      } else {
        // Email registration
        auth.showMessage("Success! We've sent an activation email to your inbox. Activate now for seamless login!", 'success')
      }
      auth.changeForm('login')
      // user.$patch({
      //   username: auth.fields.username,
      //   auth: false,
      //   success: true
      // })
      // toast.$patch({
      //   message: "Success! You're now a valued member of our community.",
      //   color: 'success',
      //   open: true
      // })
      // user.getDetails()
      // storeTokens(response, 'register')
      // reset clientstore here if allowing to app after register
      firebaseSignOut()
    }
  })

  onError(() => {
    auth.processState(false)
    toast.$patch({
      message: errorToastMsg,
      color: 'danger',
      open: true
    })
  })
}

function checkUserDetails() {
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
          username: auth.fields.username,
          password1: auth.fields.password1,
          password2: auth.fields.password2,
          ...auth.emailOrPhone,
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  onDone(async ({data}) => {
    if (data.userCheck.success) {
      const response = await auth.sendOTP()
      // Show verification popup
      if (response.success) {
        auth.changeForm('verify', register)
      } else {
        auth.errors = ['Verification code failed to send. Please retry!']
      }
    } else {
      auth.errors = data.userCheck.errors
    }
    auth.processState(false)
  })

  onError(() => {
    auth.processState(false)
  })
}
</script>

<style lang="scss" scoped>

.register-form {
  --ion-grid-column-padding: 6px;
}

</style>