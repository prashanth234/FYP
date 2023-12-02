<template>
  <ion-grid class="otp-grid">
    <ion-row class="ion-text-center">

      <ion-col size="12">
        <h3 class="ion-no-margin">{{ props.title || "Verify Account" }}</h3>
      </ion-col>

      <slot></slot>

      <ion-col size="12" class="ion-padding-vertical">
        Enter the code we just sent to your mobile phone <a class="cpointer auth-link" :class="{'cursor-disable': auth.processing}" @click="auth.goPreviousForm()">+91 {{ auth.fields.emailphone }}</a>
      </ion-col>

      <ion-col size="12">
        <otp-input v-model="auth.fields.otp" :digit-count="6"></otp-input>
      </ion-col>

      <ion-col size="12" v-if="auth.errors.length">
        <errors :errors="auth.errors"/>
      </ion-col>

      <ion-col size="11" class="ion-padding-vertical" style="margin: auto;">
        <ion-button class="auth-button" color="primary" :disabled="auth.processing" expand="block" @click="submit()">
          Submit
        </ion-button>
      </ion-col>

    </ion-row>
  </ion-grid>
</template>

<script lang="ts" setup>
import otpInput from '@/components/OTPInputContainer.vue';
import { IonCol, IonRow, IonButton, IonGrid } from '@ionic/vue';
import errors from './ErrorContainer.vue';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();

const emit = defineEmits<{
  (e: 'editphone'): void;
  (e: 'verified', user: any): void
}>()

const props = defineProps({
  title: {
    type: String,
    required: false
  }
})

async function submit() {
  const invalidError = "Invalid code. Check the OTP on your mobile."

  if (auth.fields.otp.length != 6) {
    auth.errors = [invalidError]
    return
  }

  auth.processState(true)

  try {
    const response = await auth.otpVerifier.confirm(auth.fields.otp)
    auth.postVerify && auth.postVerify(response.user)
  } catch (error: any) {
    if (error?.code == 'auth/invalid-verification-code') {
      auth.errors = [invalidError]
    } else {
      auth.errors = ["Verification failed. Please try again."]
    }
    auth.processState(false)
  }
}

</script>

<style lang="scss" scoped>

</style>