<template>

  <!-- Start of login form -->
  <form @submit.prevent="submitForm">
    <ion-grid class="login-form">

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
          <ion-input
            class="custom-input"
            v-model="fields.emailphone"
            type="text"
            placeholder="Email or Phone"
            required
          >
          </ion-input>
          <!-- <div class="ion-text-start input-error-text" v-if="error.emailphone">
            Invalid email or phone
          </div> -->
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="fields.password1"
            type="password"
            placeholder="Password"
            autocomplete="current-password"
            required
          >
          </ion-input>
        </ion-col>

        <ion-col size="12" v-if="state.errors.length">
          <ion-text>
            <ul class="ul-error-text">
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

        <ion-col size="12" class="line" style="margin-top: 10px; margin-bottom: 8px;"></ion-col>

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
          <ion-button :disabled="processing" class="register-button" size="small" color="success" @click="register()">Create Account</ion-button>
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
import { storeTokens, useAuth } from '@/composables/auth'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

interface State {
  errors: string[],
  forgotPassLoading: boolean,
  loginLoading: boolean
}

const state: State = reactive({
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
const {fields, valid, getEmailOrPhone} = useAuth();

function isValidEmail() {
  if (!valid.value.emailphone) {
    state.errors = [`Please enter valid email or phone`]
    return false
  }
  return true
}

function forgotPassword () {

  if (!isValidEmail()) { return }
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
          ...getEmailOrPhone()
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

  if (!isValidEmail()) { return }
  state.loginLoading = true
  state.errors = []

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
          ...getEmailOrPhone(),
          password: fields.password1
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