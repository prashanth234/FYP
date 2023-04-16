<template>

  <!-- Start of register form -->
  <ion-grid>

    <ion-row>
      
      <ion-col size="12">
        <ion-title>Create Account</ion-title>
      </ion-col>

      <!-- <ion-col size="6">
        <ion-input class="custom-input" v-model="state.firstname" type="text" placeholder="First Name"></ion-input>
      </ion-col>
      <ion-col size="6">
        <ion-input class="custom-input" v-model="state.lastname" type="text" placeholder="Last Name"></ion-input>
      </ion-col> -->

      <ion-col size="12">
        <ion-input class="custom-input" v-model="state.email" type="text" placeholder="Email"></ion-input>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" v-model="state.username" type="text" placeholder="Username"></ion-input>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" v-model="state.password1" type="password" placeholder="Password"></ion-input>
      </ion-col>

      <ion-col size="12">
        <ion-input class="custom-input" v-model="state.password2" type="password" placeholder="Confirm Password"></ion-input>
      </ion-col>

      <!-- <ion-col size="6">
        <ion-input class="custom-input" v-model="state.dob" @click="controlDOB(true)" type="text" placeholder="Birth Date"></ion-input>
        <ion-popover :is-open="state.isOpen">
          <ion-datetime @ionCancel="controlDOB(false)" @ionChange="changeDOB" :show-default-buttons="true" presentation="date"></ion-datetime>
        </ion-popover>
      </ion-col>

      <ion-col size="6">
        <ion-select v-model="state.gender" class="custom-select" interface="popover" placeholder="Gender">
          <ion-select-option value="male">Male</ion-select-option>
          <ion-select-option value="female">Female</ion-select-option>
          <ion-select-option value="others">Others</ion-select-option>
        </ion-select>
      </ion-col> -->

      <ion-col size="12" v-if="state.errors.length">
        <ion-text color="danger">
          <ul style="padding-left: 15px">
            <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
          </ul>
        </ion-text>
      </ion-col>

      <ion-col size="12">
        <ion-button color="primary" :disabled="state.disabled" expand="block" @click="submitForm()">Register</ion-button>
      </ion-col>

      <ion-col size="12">
        Have an account? <a class="cpointer" @click="goToLogin()">Log in</a>
      </ion-col>

    </ion-row>

  </ion-grid>
  <!-- End of register form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonText, IonPopover, IonDatetime, IonSelect, IonSelectOption, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import store from '@/vuex'

interface DatetimeChangeEventDetail {
  detail: {
    value: string
  }
}

const emit = defineEmits<{
  (e: 'login'): void
}>()

const state = reactive({
  username: '',
  password1: '',
  password2: '',
  email: '',
  firstname: '',
  lastname: '',
  dob: '',
  gender: '',
  disabled: false,
  isOpen: false,
  errors: []
})

const ionRouter = useIonRouter();

function controlDOB(value: boolean) {
  state.isOpen = value
}

function changeDOB(event: DatetimeChangeEventDetail) {
  state.dob = event.detail.value.substring(0, 10)
  controlDOB(false)
}

function goToLogin() {
  emit('login')
}

function submitForm () {

  state.disabled = true

  const { mutate, onDone } = useMutation(gql`
       mutation ($email: String!, $username: String!, $password1: String!, $password2: String!) {
        register (
          email: $email,
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
          username: state.username,
          password1: state.password1,
          password2: state.password2,
          email: state.email
        }
      }
  )

  mutate()

  onDone((result) => {
    state.disabled = false
    const response = result.data.register
    if (response.errors) {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}) => {
          state.errors.push(message)
        })
      })
    } else if (response.success) {
      localStorage.setItem('fyptoken', response.token)
      localStorage.setItem('fyprefreshtoken', response.refreshToken)
      response.user = { username: state.username }
      store.commit('storeUser', response)
      ionRouter.push('/category')
    }
  })
}
</script>