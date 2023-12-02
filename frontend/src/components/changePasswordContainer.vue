<template>

  <form @submit.prevent="verifyAccount" id="forgot-password">

    <ion-grid class="change-password-form">
      <ion-row class="ion-padding-top">

        <ion-col
          size="12"
          class="ion-padding-bottom ion-text-center auth-header"
        >
          Password Reset
        </ion-col>

        <ion-col size="12" class="ion-padding-top">
          <ion-input
            class="custom-input"
            v-model="auth.fields.password1"
            type="password"
            placeholder="New Password"
            autocomplete="new-password"
          ></ion-input>
        </ion-col>

        <ion-col size="12">
          <ion-input
            class="custom-input"
            v-model="auth.fields.password2"
            type="password"
            placeholder="Confirm Password"
            autocomplete="new-password"
          ></ion-input>
        </ion-col>

        <ion-col size="12" class="ion-no-padding">
          <errors :errors="auth.errors"/>
        </ion-col>

        <ion-col size="12" class="ion-padding-vertical" style="margin: auto;" v-if="props.hideIonButton">
          <input
            id="recaptcha-verifier"
            type="submit"
            value="Verify & Reset"
            class="auth-button input-auth-button"
            :class="{'disable-button': auth.processing}"
          >
        </ion-col>

        <ion-col size="12" v-else>
          <ion-button
            class="auth-button"
            color="primary"
            expand="block"
            @click="emit('submit')"
            :disabled="auth.processing"
          >
            <ion-spinner 
              class="button-loading-small"
              v-if="auth.processing"
              name="crescent"
            />
            <span v-else>
              Submit
            </span>
          </ion-button>
        </ion-col>

      </ion-row>
    </ion-grid>

  </form>
</template>

<script lang="ts" setup>
import { IonCol, IonGrid, IonRow, IonInput, IonButton, IonSpinner } from '@ionic/vue';
import { useAuthStore } from '@/stores/auth';
import errors from './errorContainer.vue';
import gql from 'graphql-tag';
import { useMutation } from '@vue/apollo-composable';
import { useToastStore } from '@/stores/toast';
import { useRecaptchaVerifier } from '@/composables/auth'

const auth = useAuthStore()
const toast = useToastStore()

const props = defineProps({
	hideIonButton: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits<{
  (e: 'submit'): void;
}>()

useRecaptchaVerifier()

async function verifyAccount() {
  if (auth.fields.password1.toLocaleLowerCase() != auth.fields.password2.toLocaleLowerCase()) {
    auth.errors = ["The two password fields didn’t match."]
    return
  }

  if (auth.fields.password1.length < 9) {
    auth.errors = ["The password must contain at least 9 characters."]
    return
  }

  auth.processState(true)

  const response = await auth.sendOTP()

  // Show verification popup
  if (response.success) {
    auth.changeForm('verify', changePassword)
  } else {
    auth.errors = ['Verification code failed to send. Please retry!']
  }

  auth.processState(false)
}

function changePassword(user: any) {
  const {password1, password2} = auth.fields
  auth.processState(true)

  const { mutate, onDone, onError } = useMutation(gql`
    mutation ($token: String!, $newPassword1: String!, $newPassword2: String!)  {
      changePassword(
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
        token: user.accessToken,
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
      auth.message = 'Password reset successful! You can now log in using your new password.'
      auth.changeForm('login')
    } else {
      const keys = Object.keys(response.errors)
      keys.forEach(key => {
        response.errors[key].forEach(({message}:{message: string}) => {
          auth.errors.push(message)
        })
      })
    }

    onError(() => {
      toast.$patch({
        message: "Password reset failed. If the issue persists, please contact our support team for assistance.",
        color: 'danger',
        open: true
      })
      auth.processState(false)
    })
  })
}

</script>

<style lang="scss">

.change-password-form {
  --ion-grid-column-padding: 6px;
}

</style>