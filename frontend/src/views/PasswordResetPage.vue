<template>

  <ion-page>
    <ion-content>

      <ion-grid>
        <ion-row class="ion-padding forgot-password" style="margin: auto; margin-top: 100px; padding: 25px;">
          <change-password
            @submit="submitForm"
            :hideIonButton="false"
          ></change-password>
        </ion-row>
      </ion-grid>

    </ion-content>
  </ion-page>

</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { useMutation } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { IonPage, IonContent, useIonRouter, IonGrid, IonRow } from '@ionic/vue'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import ChangePassword from '@/components/ChangePasswordContainer.vue'


const router = useRoute();
const ionRouter = useIonRouter();
const toast = useToastStore();
const auth = useAuthStore();

const token = router.params.token

function clear () {
  auth.clearErrors()
  auth.clearPasswords()
}

function submitForm () {
  const {password1, password2} = auth.fields

  auth.processState(true)

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
        newPassword1: password1,
        newPassword2: password2
      },
    }
  )

  mutate()

  onDone((result) => {
    const response = result.data.passwordReset
    auth.processState(false)

    if (response.success) {
      // goHome()
      // auth.open()
      // auth.showMessage('Password reset successful! You can now log in using your new password.', 'success')
      toast.$patch({message: "Password reset successful! You can now log in using your new password.", color: 'success', open: true})
      clear()
    } else {
      const keys = Object.keys(response.errors)
      keys.forEach(key => {
        response.errors[key].forEach((message: string) => {
          auth.errors.push(message)
        })
      })
    }

    onError(() => {
      toast.$patch({message: "Password reset failed. If the issue persists, please contact our support team for assistance.", color: 'danger', open: true})
      auth.processState(false)
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
</style>