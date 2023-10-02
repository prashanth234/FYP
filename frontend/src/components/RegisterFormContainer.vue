<template>

  <!-- Start of register form -->
  <form @submit.prevent="submitForm">
    <ion-grid>

      <ion-row class="ion-text-center">
        
        <ion-col size="12" class="ion-padding-bottom">
          <ion-title>Create Account</ion-title>
        </ion-col>

        <ion-col size="12">
          <ion-input 
            class="custom-input"
            fill="outline"
            v-model="state.email"
            type="email"
            placeholder="Email"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            fill="outline"
            v-model="state.username"
            type="text"
            placeholder="Username"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            fill="outline"
            v-model="state.password1"
            type="password"
            placeholder="Password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            fill="outline"
            v-model="state.password2"
            type="password"
            placeholder="Confirm Password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12" v-if="state.errors.length">
          <ion-text color="danger">
            <ul style="padding-left: 15px">
              <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
            </ul>
          </ion-text>
        </ion-col>

        <ion-col size="12">
          <ion-button color="primary" class="auth-button" :disabled="state.loading" expand="block" type="submit">
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

        <ion-col size="12" class="line" style="margin-top: 10px; margin-bottom: 15px;"></ion-col>

        <ion-col size="12">
          Have an account? <a class="cpointer" :class="{'cursor-disable': state.loading}" @click="goToLogin()"><b>Log in</b></a>
        </ion-col>

      </ion-row>

    </ion-grid>
  </form>
  <!-- End of register form -->

</template>

<script lang="ts" setup>

import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonTitle, IonText, IonSpinner, useIonRouter } from '@ionic/vue';
import gql from 'graphql-tag'
import { reactive, inject } from 'vue'
import { useMutation } from '@vue/apollo-composable'
import { storeTokens } from '@/mixims/auth'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user';

// import { validate, markTouched } from '@/mixims/validations'

// const validation = reactive({
//   username: false,
//   password1: false,
//   password2: false,
//   email: false,
// })

// error-text="Invalid email"
// @ionInput="validation.email = validate($event, ['email'])"
// @ionBlur="markTouched"

const emit = defineEmits<{
  (e: 'login'): void
}>()

const { isAuthProcessing, authSuccess, authFailure } = inject<any>('auth')

interface State {
  errors: Array<string>,
  username: string,
  password1: string,
  password2: string,
  email: string,
  firstname: string,
  lastname: string,
  dob: string,
  gender: string,
  loading: boolean,
  isOpen: boolean,
}

const state: State = reactive({
  username: '',
  password1: '',
  password2: '',
  email: '',
  firstname: '',
  lastname: '',
  dob: '',
  gender: '',
  loading: false,
  isOpen: false,
  errors: []
})

const ionRouter = useIonRouter();
const toast = useToastStore();
const user = useUserStore();

function goToLogin() {
  emit('login')
}

function submitForm () {

  state.errors = []
  state.loading = true
  isAuthProcessing(true)

  const { mutate, onDone, onError } = useMutation(gql`
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
      user.$patch({username: state.username, auth: false, success: true})
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