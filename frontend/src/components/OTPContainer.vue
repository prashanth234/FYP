<template>
  <ion-grid class="otp-grid">
    <ion-row class="ion-text-center">

      <ion-col size="12">
        <h3 class="ion-no-margin">{{ props.title || "Verify Account" }}</h3>
      </ion-col>

      <ion-col size="12" class="ion-padding-vertical">
        Enter the code we just sent to your mobile phone <a style="font-weight: 500;" @click="emit('editphone')">+91 {{ props.phone }}</a>
      </ion-col>

      <ion-col size="12">
        <otp-input v-model="state.otp" :digit-count="6"></otp-input>
      </ion-col>

      <slot></slot>

      <ion-col size="12" v-if="state.errors.length">
        <errors :errors="state.errors"/>
      </ion-col>

      <ion-col size="11" class="ion-padding-vertical" style="margin: auto;">
        <ion-button class="auth-button" color="primary" :disabled="state.verifying" expand="block" @click="submit()">
          <ion-spinner 
            class="button-loading-small"
            v-if="state.verifying"
            name="crescent"
          />
          <span v-else>
            Submit
          </span>
        </ion-button>
      </ion-col>

    </ion-row>
  </ion-grid>
</template>

<script lang="ts" setup>
import otpInput from '@/components/OTPInputContainer.vue';
import { IonCol, IonRow, IonButton, IonSpinner, IonGrid } from '@ionic/vue';
import { reactive } from 'vue';
import errors from './errorContainer.vue';

interface State {
  verifying: boolean,
  otp: string,
  errors: Array<string>
}

const state: State = reactive({
  verifying: false,
  otp: '',
  errors: []
})

const emit = defineEmits<{
  (e: 'editphone'): void;
  (e: 'submitOTP', otp: string, postVerify: any): void
}>()

const props = defineProps({
  phone: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: false
  }
})

function postVerify(response: {success: boolean, error: any}) {
  if (response.error) {
    if (response.error.code == 'auth/invalid-verification-code') {
      state.errors = ["Invalid code. Check the OTP on your mobile."]
    } else {
      state.errors = ["Verification failed. Please try again."]
    }
  }
  state.verifying = false
}

function submit() {
  state.errors = []
  state.verifying = true
  emit('submitOTP', state.otp, postVerify)
}

</script>

<style lang="scss" scoped>

</style>