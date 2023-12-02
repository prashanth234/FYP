<template>

  <!-- Start of login form -->
  <form @submit.prevent="submitForm" id="login-form">

    <ion-grid class="login-form">

      <ion-row class="ion-text-center">

        <ion-col size="12">
          <ion-title>TBD</ion-title>
        </ion-col>

        <ion-col v-if="auth.message">
          <ion-card
            class="note-card"
            style="margin: 0px !important;"
            color="light"
          >
            <ion-card-content class="ion-text-center" style="font-weight: 500;">
              {{ auth.message }}
            </ion-card-content>
          </ion-card>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="auth.fields.emailphone"
            type="text"
            placeholder="Email or Phone"
            required
            ref="emailphoneref"
            autofocus
          >
          </ion-input>
          <!-- <div class="ion-text-start input-error-text" v-if="error.emailphone">
            Invalid email or phone
          </div> -->
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="auth.fields.password1"
            type="password"
            placeholder="Password"
            autocomplete="current-password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12" class="ion-no-padding">
          <errors :errors="auth.errors"/>
        </ion-col>

        <ion-col size="12">
          <ion-button
            class="auth-button"
            color="primary"
            :disabled="auth.processing"
            expand="block"
            type="submit"
          >
            Login
          </ion-button>
        </ion-col>

        <ion-col size="12" class="line" style="margin-top: 10px; margin-bottom: 8px;"></ion-col>

        <ion-col size="12" >
          <ion-button
            fill="clear"
            @click="forgotPassword"
            :disabled="auth.processing"
          >
            Forgotten password?
          </ion-button>
        </ion-col>
        
        <ion-col size="12">
          <ion-button
            :disabled="auth.processing"
            class="register-button"
            size="small"
            color="success"
            @click="register()"
          >
            Create Account
          </ion-button>
        </ion-col>
        
      </ion-row>

    </ion-grid>

  </form>
  <!-- End of login form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonCard, IonCardContent } from '@ionic/vue';
import gql from 'graphql-tag'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens, useAuth } from '@/composables/auth'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import errors from './ErrorContainer.vue'
import { useAuthStore } from '@/stores/auth'

const user = useUserStore();
const toast = useToastStore();
const auth = useAuthStore();
const {
  emailphoneref,
  focusEmailPhone,
  resetClientStore
} = useAuth();

function editphone() {
  auth.changeForm('login')
  auth.clearPasswords()
  focusEmailPhone()
}

function forgotPassword () {

  if (!auth.isValidEmailPhone()) {
    return
  }

  if (auth.isInputPhone) {
    auth.changeForm('change-password')
    return
  }
  
  auth.processState(true)

  const { mutate, onDone, onError } = useMutation(gql`    
      mutation ($email: String!) {
        sendPasswordResetEmail (
            email: $email
          ) {
            success,
            errors
          }
      }
    `,{
        // Parameters
        variables: {
          email: auth.fields.emailphone
        }
      }
  )

  mutate()

  onDone(({data: {sendPasswordResetEmail}}) => {
    if (sendPasswordResetEmail.success) {
      // toast.$patch({message: "An email with a password reset link will be sent to you shortly.", color: 'success', open: true})
      auth.message = 'Password reset link sent to your email. Kindly proceed to reset and log in.'
    } else {
      toast.$patch({message: "Apologies, but we couldn't send the password reset link to your email. Please try again.", color: 'danger', open: true})
    }
    auth.processState(false)
  })

  onError(() => {
    toast.$patch({message: "We're experiencing technical difficulties with our email service. Please try again later.", color: 'danger', open: true})
    auth.processState(false)
  })
}

function submitForm () {

  if (!auth.isValidEmailPhone()) { return }
  
  auth.processState(true)

  // Also me Query when this query is updated
  const { mutate, onDone, onError } = useMutation(gql`    
      mutation Login ($email: String, $phone: String, $password: String!) {
        tokenAuth(email: $email, phone: $phone, password: $password) {
          success,
          errors,
          unarchiving,
          token,
          refreshToken,
          user {
            username,
            firstName,
            lastName,
            email,
            phone,
            gender,
            avatar,
            points,
            verified
          }
        }
      }

    `,{
        // Parameters
        variables: {
          ...auth.emailOrPhone,
          password: auth.fields.password1
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  onDone((result) => {
    const response = result.data.tokenAuth

    if (response.success) {
      storeTokens(response, 'login')
      resetClientStore()
      user.$patch({
        ...response.user,
        userUpdated: user.userUpdated + 1,
        success: true
      })
      auth.close()
      toast.$patch({
        message: `Success! Welcome, ${response.user.username}!`,
        color: 'success',
        open: true
      })
    } else {
      const keys = Object.keys(response.errors)
      keys.forEach(key => {
        response.errors[key].forEach(({message}:{message: string}) => {
          auth.errors.push(message)
        })
      })
    }
    auth.processState(false)
  })

  onError(() => {
    toast.$patch({message: "Login failed due to technical difficulties. Please try again later.", color: 'danger', open: true})
    auth.processState(false)
  })
}

function register() {
  auth.discardMessage()
  auth.changeForm('register')
}

</script>

<style lang="scss" scoped>
@media only screen and (max-width: 576px) {
	.register-button {
    height: 30px;
  }
}

.login-form {
  --ion-grid-column-padding: 6px;
}
</style>