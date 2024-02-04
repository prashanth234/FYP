<template>
  <ion-toast
    position="top"
    :color="toast.color"
    :is-open="toast.open"
    :message="toast.message"
    :duration="5000"
    @didDismiss="toast.open = false"
    :buttons="toastButtons"
  ></ion-toast>
</template>

<script lang="ts" setup>

import { IonToast } from '@ionic/vue'
import { ref } from 'vue'
import { useToastStore } from '@/stores/toast'
// import { closeOutline } from 'ionicons/icons'

const toastButtons = ref([
        {
          text: 'Dismiss',
          role: 'cancel'
        }
      ])

const toast = useToastStore()

</script>

<style scoped>
ion-toast.custom-toast {
  --background: #F4F4FA;
  --box-shadow: 3px 3px 10px 0 rgba(0, 0, 0, 0.2);
  --color: #4b4a50;
}
  
ion-toast.custom-toast::part(message) {
  font-style: italic;
}

ion-toast.custom-toast::part(button) {
  border-left: 1px solid #d2d2d2;
  color: #030207;
  font-size: 15px;
}
</style>