<template>

  <!-- Start of login form -->
  <form @submit.prevent="submitForm">
    <ion-grid>

      <ion-row class="ion-text-center">

        <ion-col size="12">
          <ion-title>TBD</ion-title>
        </ion-col>

        <ion-col v-if="user.authMessage">
          <ion-card
            class="note-card"
            style="margin: 0px !important;"
            color="light"
          >
            <ion-card-content class="ion-text-center" style="font-weight: 500;">
              {{ user.authMessage }}
            </ion-card-content>
          </ion-card>
        </ion-col>

        <ion-col size="12">
          <ion-input class="custom-input" fill="outline" v-model="state.email" type="email" placeholder="Email" required></ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input class="custom-input" fill="outline" v-model="state.password" type="password" placeholder="Password" required></ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-text color="danger" v-if="state.errors.length">
            <ul style="padding-left: 15px">
              <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
            </ul>
          </ion-text>
        </ion-col>

        <ion-col size="12">
          <ion-button class="auth-button" color="primary" :disabled="processing" expand="block" type="submit">
            <ion-spinner 
              class="button-loading-small"
              v-if="state.loginLoading"
              name="crescent"
            />
            <span v-else>
              Login
            </span>
          </ion-button>
        </ion-col>

        <ion-col size="12" class="line" style="margin-top: 12px; margin-bottom: 10px;"></ion-col>

        <ion-col size="12" >
          <ion-button fill="clear" @click="forgotPassword" :disabled="processing">
            <ion-spinner 
              class="button-loading-small"
              v-if="state.forgotPassLoading"
              name="crescent"
            />
            <span v-else>
              Forgotten password?
            </span>
          </ion-button>
        </ion-col>
        
        <ion-col size="12">
          <ion-button :disabled="processing" size="small" color="success" @click="register()">Create Account</ion-button>
        </ion-col>
        
      </ion-row>

    </ion-grid>
  </form>
  <!-- End of login form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonText, IonSpinner, IonCard, IonCardContent, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, computed, inject } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens } from '@/mixims/auth'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

interface State {
  email: string,
  password: string,
  errors: string[],
  forgotPassLoading: boolean,
  loginLoading: boolean
}

const state: State = reactive({
  email: '',
  password: '',
  loginLoading: false,
  errors: [],
  forgotPassLoading: false,
})

const { isAuthProcessing, authSuccess, authFailure } = inject<any>('auth')

const processing = computed(() => {
  const process = state.loginLoading || state.forgotPassLoading
  isAuthProcessing(process)
  return process
})


const emit = defineEmits<{
  (e: 'register'): void
}>()

const ionRouter = useIonRouter();
const user = useUserStore();
const toast = useToastStore();

function forgotPassword () {

  if (!state.email) {
    state.errors = ["Please enter the email"]
    return
  }

  state.forgotPassLoading = true
  state.errors = []

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
          email: state.email
        }
      }
  )

  mutate()

  onDone(({data: {sendPasswordResetEmail}}) => {
    if (sendPasswordResetEmail.success) {
      toast.$patch({message: "Password reset email sent successfully!", color: 'success', open: true})
    }
    state.forgotPassLoading = false
  })

  onError(() => {
    toast.$patch({message: "We're experiencing technical difficulties with our email service. Please try again later.", color: 'danger', open: true})
    state.forgotPassLoading = false
  })
}

function submitForm () {

  state.loginLoading = true

  // Also update user details when this query is updated
  const { mutate, onDone, onError } = useMutation(gql`    
      mutation Login ($email: String!, $password: String!) {
        tokenAuth(email: $email, password: $password) {
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
          email: state.email,
          password: state.password
        },
        fetchPolicy: "no-cache"
      }
  )

  mutate()

  onDone((result) => {
    const response = result.data.tokenAuth
    state.loginLoading = false

    if (response.success) {
      storeTokens(response, 'login')
      authSuccess('login')
      user.$patch({...response.user, userUpdated: user.userUpdated + 1, success: true, auth: false, authMessage: ''})
      toast.$patch({message: `Success! Welcome, ${response.user.username}!`, color: 'success', open: true})
    } else {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}:{message: string}) => {
          state.errors.push(message)
        })
      })
      authFailure('login')
    }
  })

  onError(() => {
    toast.$patch({message: "Login failed due to technical difficulties. Please try again later.", color: 'danger', open: true})
    state.loginLoading = false
    authFailure('login')
  })
}

function register() {
  emit('register')
  user.authMessage = ''
}

</script>