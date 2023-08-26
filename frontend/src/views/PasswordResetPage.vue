<template>

  <ion-page>
    <ion-content>

      
        <ion-grid>
          <ion-row class="ion-padding forgot-password" style="margin: auto; margin-top: 100px; padding: 25px;">

            <ion-col size="12" class="ion-text-center">
              <h3>Reset Password</h3>
            </ion-col>

            <ion-col size="12">
              <ion-input class="custom-input" fill="outline" v-model="state.newPassword1" type="password" placeholder="New Password"></ion-input>
            </ion-col>

            <ion-col size="12">
              <ion-input class="custom-input" fill="outline" v-model="state.newPassword2" type="password" placeholder="Confirm Password"></ion-input>
            </ion-col>

            <ion-col size="12" v-if="state.errors.length">
              <ion-text color="danger">
                <ul style="padding-left: 15px">
                  <li v-for="(message, index) in state.errors" :key="index">{{message}}</li>
                </ul>
              </ion-text>
            </ion-col>

            <ion-col size="12">
              <ion-button class="auth-button" color="primary" :disabled="state.reseting" expand="block" @click="submitForm()">
                <ion-spinner 
                  class="button-loading-small"
                  v-if="state.reseting"
                  name="crescent"
                />
                <span v-else>
                  Submit
                </span>
              </ion-button>
            </ion-col>

          </ion-row>
        </ion-grid>
    </ion-content>
  </ion-page>

</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { reactive } from 'vue'
import { IonPage, IonContent, IonGrid, IonRow, IonCol, IonInput, IonButton, IonSpinner, IonText, IonTitle, useIonRouter } from '@ionic/vue'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'


const router = useRoute();
const ionRouter = useIonRouter();
const toast = useToastStore();
const user = useUserStore();

const token = router.params.token

interface State {
  newPassword1: string,
  newPassword2: string,
  errors: string[],
  reseting: boolean
}

const state: State = reactive({
  newPassword1: '',
  newPassword2: '',
  reseting: false,
  errors: []
})

function clear () {
  state.newPassword1 = ''
  state.newPassword2 = ''
  state.errors = []
}

function submitForm () {
  const {newPassword1, newPassword2} = state

  state.reseting = true

  const { mutate, onDone, onError } = useMutation(gql`
    mutation ($token: String!, $newPassword1: String!, $newPassword2: String!)  {
      passwordReset(
          token: $token,
          newPassword1: $newPassword1,
          newPassword2: $newPassword2
        ) {
          success,
          errors
        }
    }
  `,
    {
      variables: {
        token,
        newPassword1,
        newPassword2
      },
    }
  )

  mutate()

  onDone((result) => {
    const response = result.data.passwordReset
    state.reseting = false

    if (response.success) {
      toast.$patch({message: 'Password reset successful! You can now log in using your new password.', color: 'success', open: true})
      // user.auth = true
      // goHome()
      clear()
    } else {
      const keys = Object.keys(response.errors)
      state.errors = []
      keys.forEach(key => {
        response.errors[key].forEach(({message}:{message: string}) => {
          state.errors.push(message)
        })
      })
    }

    onError(() => {
      toast.$patch({message: "Password reset failed. If the issue persists, please contact our support team for assistance.", color: 'danger', open: true})
      state.reseting = false
    })
  })
}

function goHome () {
  ionRouter.push('/')
}

</script>

<style lang="scss" scoped>
@media only screen and (min-width: 576px) {
  // For sm and above screens
  .forgot-password {
    max-width: 350px;
    border: 1px solid var(--ion-color-light-shade);
  }
}
ion-grid {
  --ion-grid-column-padding: 10px
}
</style>