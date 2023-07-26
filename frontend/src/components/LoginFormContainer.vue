<template>

  <!-- Start of login form -->
  <ion-grid>

    <ion-row class="ion-text-center">

      <ion-col size="12">
        <ion-title>TBD</ion-title>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" fill="outline" v-model="state.email" type="email" placeholder="Email"></ion-input>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" fill="outline" v-model="state.password" type="password" placeholder="Password"></ion-input>
      </ion-col>

      <ion-col size="12">
        <ion-text color="danger" v-if="state.errors.length">
          <ul style="padding-left: 15px">
            <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
          </ul>
        </ion-text>
      </ion-col>

      <ion-col size="12">
        <ion-button class="auth-button" color="primary" :disabled="state.disabled" expand="block" @click="submitForm()">Login</ion-button>
      </ion-col>

      <ion-col size="12" class="line" style="margin-top: 12px; margin-bottom: 10px;"></ion-col>

      <ion-col size="12" >
        <ion-button fill="clear" @click="forgotPassword">Forgotten password?</ion-button>
      </ion-col>
      
      <ion-col size="12">
        <ion-button :disabled="state.disabled" size="small" color="success" @click="register()">Create Account</ion-button>
      </ion-col>
      
    </ion-row>

  </ion-grid>
  <!-- End of login form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonText, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens } from '@/mixims/auth'
import store from '@/vuex'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

interface State {
  email: string,
  password: string,
  disabled: boolean,
  errors: string[]
}

const state: State = reactive({
  email: '',
  password: '',
  disabled: false,
  errors: []
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

  const { mutate, onDone } = useMutation(gql`    
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
      toast.$patch({message: "Email sent successfully", color: 'success', open: true})
    }
  })
}

function submitForm () {

  state.disabled = true

  const { mutate, onDone } = useMutation(gql`    
      mutation ($email: String!, $password: String!) {
        tokenAuth(email: $email, password: $password) {
          success,
          errors,
          unarchiving,
          token,
          refreshToken,
          unarchiving,
          user {
            id,
            username,
            avatar,
          }
        }
      }

    `,{
        // Parameters
        variables: {
          email: state.email,
          password: state.password
        }
      }
  )

  mutate()

  onDone((result) => {
    const response = result.data.tokenAuth
    state.disabled = false

    if (response.success) {
      storeTokens(response, 'login')
      user.$patch({...response.user, success: true, userUpdated: user.userUpdated + 1, auth: false})
      toast.$patch({message: 'Login Successful', color: 'success', open: true})
      // ionRouter.push('/')
    } else {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}:{message: string}) => {
          state.errors.push(message)
        })
      })
    }
  })
}

function register() {
  emit('register')
}

</script>