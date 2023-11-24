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

      <ion-col size="12">
        <slot></slot>
      </ion-col>

      <ion-col size="11" class="ion-padding-vertical" style="margin: auto;">
        <ion-button class="auth-button" color="primary" :disabled="state.verifying" expand="block" @click="verify()">
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
import otpInput from '@/components/OTPInputContainer.vue'
import { IonCol, IonRow, IonButton, IonSpinner, IonGrid } from '@ionic/vue';
import { reactive } from 'vue';

const state = reactive({
  verifying: false,
  otp: ''
})

const emit = defineEmits<{
  (e: 'editphone'): void;
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

function verify() {

}

</script>

<style lang="scss" scoped>

</style>