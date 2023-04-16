<template>

  <!-- Start of login form -->
  <ion-grid>

    <ion-row>

      <ion-col size="12">
        <ion-title>TBD</ion-title>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" fill="outline" v-model="state.username" type="text" placeholder="Username"></ion-input>
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
        <ion-button color="primary" :disabled="state.disabled" expand="block" @click="submitForm()">Login</ion-button>
      </ion-col>

      <ion-col size="12">
        <a>Forgotten password?</a>
      </ion-col>
      
      <ion-col size="12">
        <ion-button :disabled="state.disabled" size="small" color="success" @click="register()">Create Account</ion-button>
      </ion-col>
      
    </ion-row>

  </ion-grid>
  <!-- End of login form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonCard, IonButton, IonTitle, IonText, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import store from '@/vuex'

const state = reactive({
  username: '',
  password: '',
  disabled: false,
  errors: []
})

const emit = defineEmits<{
  (e: 'register'): void
}>()

const ionRouter = useIonRouter();

function submitForm () {

  state.disabled = true

  const { mutate, onDone } = useMutation(gql`    
      mutation ($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
          success,
          errors,
          unarchiving,
          token,
          refreshToken,
          unarchiving,
          user {
            id,
            username,
          }
        }
      }

    `,{
        // Parameters
        variables: {
          username: state.username,
          password: state.password
        }
      }
  )

  mutate()

  onDone((result) => {
    const response = result.data.tokenAuth
    state.disabled = false

    if (response.success) {
      localStorage.setItem('fyptoken', response.token)
      localStorage.setItem('fyprefreshtoken', response.refreshToken)
      store.commit('storeUser', response)
      ionRouter.push('/')
    } else {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}) => {
          state.errors.push(message)
        })
      })
    }
  })
}

function register() {
  // ionRouter.push('/register')
  emit('register')
}

</script>